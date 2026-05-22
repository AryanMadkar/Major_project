# =====================================================
# utils/audio.py — Audio loading, validation, VAD
# (Voice Activity Detection) preprocessing, and
# writing optimised WAV files ready for model input.
# =====================================================

import os
import contextlib
import wave

import torch
import torchaudio

# soundfile is the preferred WAV I/O library;
# we import it with a fallback so the app doesn't
# crash if it isn't installed.
try:
    import soundfile as sf
except Exception:
    sf = None  # handled gracefully wherever sf is used


# ── Audio constants ─────────────────────────────────
# All models expect 16 kHz mono audio.
TARGET_SAMPLE_RATE = 16_000

# Use GPU when available; otherwise fall back to CPU.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ── Validation ──────────────────────────────────────

def validate_audio_file(audio_path: str) -> None:
    """
    Raise a clear error early if the file is missing,
    not a WAV, or has an unsupported encoding.
    This saves confusing errors deep inside model code.
    """

    # 1. File must actually exist on disk
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # 2. Only WAV files are supported by every downstream model
    if not audio_path.lower().endswith(".wav"):
        raise ValueError(
            f"Only WAV files are supported. "
            f"Please convert your file to WAV first: {audio_path}"
        )

    # 3. Verify the encoding is PCM (uncompressed).
    #    We try three readers in order of preference.
    encoding   = None
    sample_rate = None

    # Attempt 1 — torchaudio.info (fast, works on most installs)
    if hasattr(torchaudio, "info"):
        try:
            info        = torchaudio.info(audio_path)
            encoding    = getattr(info, "encoding", None)
            sample_rate = getattr(info, "sample_rate", None)
        except Exception:
            encoding = None  # will try next reader

    # Attempt 2 — soundfile (handles edge-case WAV variants)
    if encoding is None and sf is not None:
        try:
            info        = sf.info(audio_path)
            encoding    = getattr(info, "subtype", None)   # e.g. "PCM_16"
            sample_rate = getattr(info, "samplerate", None)
        except Exception:
            encoding = None

    # Attempt 3 — stdlib wave module (always available, basic PCM only)
    if encoding is None:
        try:
            with contextlib.closing(wave.open(audio_path, "rb")) as wf:
                sampwidth   = wf.getsampwidth()   # bytes per sample
                sample_rate = wf.getframerate()
                # 1/2/4-byte samples → standard PCM
                encoding = "PCM_S" if sampwidth in (1, 2, 4) else None
        except Exception as exc:
            raise ValueError(
                f"Could not open audio file — it may be corrupted: {audio_path}"
            ) from exc

    # If none of the readers could determine the encoding it's unsupported
    if encoding is None or "PCM" not in str(encoding).upper():
        raise ValueError(
            f"Unsupported WAV encoding '{encoding}'. "
            f"Please re-encode to PCM WAV: {audio_path}"
        )


# ── Core preprocessing ──────────────────────────────

def preprocess_audio(audio_path: str) -> torch.Tensor:
    """
    Load a WAV file and return a clean speech-only tensor.

    Pipeline:
        validate → load → stereo→mono → resample → normalise
        → VAD (remove silence) → return tensor on DEVICE
    """

    # Step 1 — Validate before touching heavy model code
    validate_audio_file(audio_path)

    # Step 2 — Load the waveform
    #   torchaudio.load returns (waveform, sample_rate)
    #   waveform shape: (channels, samples)
    try:
        waveform, sample_rate = torchaudio.load(audio_path)
    except Exception as exc:
        # Some torchaudio builds use torchcodec which may not be installed;
        # fall back to soundfile in that case.
        if sf is not None:
            try:
                data, sample_rate = sf.read(audio_path, dtype="float32")
            except Exception as exc2:
                raise RuntimeError(
                    f"Failed to read audio with both torchaudio and soundfile: {exc2}"
                ) from exc2

            import numpy as np
            arr      = np.asarray(data)                  # (samples,) or (samples, ch)
            arr      = np.expand_dims(arr, 0) if arr.ndim == 1 else arr.T
            waveform = torch.from_numpy(arr)             # (channels, samples)
        else:
            raise RuntimeError(
                "torchaudio failed and soundfile is not installed. "
                "Install soundfile: pip install soundfile"
            ) from exc

    # Step 3 — Convert stereo (or multi-channel) to mono
    #   Average across the channel dimension.
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)   # (1, samples)

    # Step 4 — Resample to TARGET_SAMPLE_RATE if needed
    if sample_rate != TARGET_SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate,
            new_freq=TARGET_SAMPLE_RATE
        )
        waveform = resampler(waveform)

    # Step 5 — Peak normalise to [-1, 1]
    #   Prevents loudness differences from affecting embeddings.
    max_val = waveform.abs().max()
    if max_val > 0:                                      # guard against silent files
        waveform = waveform / max_val

    # Step 6 — Voice Activity Detection (VAD)
    #   Strips silence and noise; models perform better on pure speech.
    try:
        from silero_vad import load_silero_vad, get_speech_timestamps
    except ImportError as exc:
        raise ImportError(
            "silero_vad is required. Install it with: pip install silero-vad"
        ) from exc

    VAD_MODEL = load_silero_vad()
    speech_timestamps = get_speech_timestamps(
        waveform.squeeze(),          # VAD expects a 1-D tensor
        VAD_MODEL,
        sampling_rate=TARGET_SAMPLE_RATE
    )

    # If no speech was found the recording is unusable
    if not speech_timestamps:
        raise ValueError(
            f"No speech detected in: {audio_path}. "
            "Check that the recording contains audible voice."
        )

    # Concatenate only the speech segments, discarding silence
    speech_chunks = [
        waveform[:, seg["start"]: seg["end"]]
        for seg in speech_timestamps
    ]
    waveform = torch.cat(speech_chunks, dim=1)           # (1, total_speech_samples)

    # Move tensor to the chosen compute device (CPU / CUDA)
    return waveform.to(DEVICE)


# ── File writer ─────────────────────────────────────

def optimize_audio_file(audio_path: str, output_dir: str) -> str:
    """
    Preprocess the audio and write the result to *output_dir*
    as a 16-bit PCM WAV at TARGET_SAMPLE_RATE.

    Returns the path of the optimised file.
    """

    os.makedirs(output_dir, exist_ok=True)

    # Build output filename: e.g. "voice_optimized.wav"
    base_name      = os.path.splitext(os.path.basename(audio_path))[0]
    optimised_path = os.path.join(output_dir, f"{base_name}_optimized.wav")

    # Run the preprocessing pipeline; move result back to CPU for saving
    waveform = preprocess_audio(audio_path).detach().cpu()

    # Convert tensor → numpy array expected by the WAV writers
    arr  = waveform.numpy()                              # (1, samples) or (ch, samples)
    data = arr.squeeze() if arr.shape[0] == 1 else arr.T  # (samples,) or (samples, ch)

    # Preferred writer: soundfile (handles float arrays cleanly)
    if sf is not None:
        data = data.astype("float32")
        sf.write(optimised_path, data, TARGET_SAMPLE_RATE, subtype="PCM_16")
        return optimised_path

    # Fallback writer: stdlib wave module (requires numpy)
    import numpy as np
    data   = data.astype("float32")
    int16  = (data * 32_767).clip(-32_768, 32_767).astype(np.int16)

    n_channels = 1 if int16.ndim == 1 else int16.shape[1]
    with contextlib.closing(wave.open(optimised_path, "wb")) as wf:
        wf.setnchannels(n_channels)
        wf.setsampwidth(2)                               # 2 bytes = 16-bit
        wf.setframerate(TARGET_SAMPLE_RATE)
        wf.writeframes(int16.tobytes())

    return optimised_path