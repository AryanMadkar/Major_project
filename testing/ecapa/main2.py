import os
import torch
import torchaudio
import torch.nn.functional as F

from functools import lru_cache
from speechbrain.pretrained import SpeakerRecognition

from silero_vad import (
    load_silero_vad,
    get_speech_timestamps
)

# =====================================================
# CONFIG
# =====================================================

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

TARGET_SAMPLE_RATE = 16000

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {DEVICE}")

# =====================================================
# LOAD MODELS
# =====================================================

verification_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="./pretrained_models",
    run_opts={"device": DEVICE},
)

vad_model = load_silero_vad()

# =====================================================
# AUDIO VALIDATION
# =====================================================

def validate_audio_file(audio_path: str):

    # File existence
    if not os.path.exists(audio_path):
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}"
        )

    # Extension validation
    if not audio_path.lower().endswith(".wav"):
        raise ValueError(
            f"Only WAV files are supported: {audio_path}"
        )

    # Real codec validation
    try:
        info = torchaudio.info(audio_path)

    except Exception:
        raise ValueError(
            f"Invalid or corrupted audio file: {audio_path}"
        )

    # Validate encoding
    if info.encoding not in [
        "PCM_S",
        "PCM_F"
    ]:
        raise ValueError(
            f"Unsupported WAV encoding: {info.encoding}"
        )

# =====================================================
# AUDIO PREPROCESSING
# =====================================================

def preprocess_audio(audio_path: str):

    validate_audio_file(audio_path)

    waveform, sample_rate = torchaudio.load(audio_path)

    # -------------------------------------------------
    # Convert stereo -> mono
    # -------------------------------------------------

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # -------------------------------------------------
    # Resample to 16kHz
    # -------------------------------------------------

    if sample_rate != TARGET_SAMPLE_RATE:

        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate,
            new_freq=TARGET_SAMPLE_RATE
        )

        waveform = resampler(waveform)

    # -------------------------------------------------
    # Loudness normalization
    # -------------------------------------------------

    waveform = waveform / waveform.abs().max()

    # -------------------------------------------------
    # Voice Activity Detection
    # -------------------------------------------------

    speech_timestamps = get_speech_timestamps(
        waveform.squeeze(),
        vad_model,
        sampling_rate=TARGET_SAMPLE_RATE
    )

    # No speech detected
    if len(speech_timestamps) == 0:
        raise ValueError(
            "No speech detected in audio."
        )

    # Keep only speech parts
    speech_segments = []

    for segment in speech_timestamps:

        start = segment["start"]
        end = segment["end"]

        speech_segments.append(
            waveform[:, start:end]
        )

    waveform = torch.cat(
        speech_segments,
        dim=1
    )

    return waveform.to(DEVICE)

# =====================================================
# CACHED EMBEDDING EXTRACTION
# =====================================================

@lru_cache(maxsize=1000)
def get_embedding(audio_path: str):

    waveform = preprocess_audio(audio_path)

    with torch.inference_mode():

        embedding = verification_model.encode_batch(
            waveform
        )

    embedding = embedding.squeeze()

    embedding = F.normalize(
        embedding,
        p=2,
        dim=0
    )

    return embedding

# =====================================================
# SPEAKER VERIFICATION
# =====================================================

def verify_speakers(
    audio1_path: str,
    audio2_path: str,
    threshold: float = 0.25
):

    try:

        emb1 = get_embedding(audio1_path)
        emb2 = get_embedding(audio2_path)

        similarity = torch.dot(
            emb1,
            emb2
        ).item()

        return {
            "success": True,
            "similarity_score": round(similarity, 4),
            "same_speaker": similarity >= threshold,
            "threshold": threshold,
            "device": DEVICE,
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "same_speaker": False,
        }

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    result = verify_speakers(
        r"D:\majorproject\testing\ecapa\audio-dataset\Ashlesha.wav",
        r"D:\majorproject\testing\ecapa\audio-dataset\aryan2.wav"
    )

    print(result)