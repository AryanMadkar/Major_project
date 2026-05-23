import torch

from silero_vad import (
    load_silero_vad,
    get_speech_timestamps
)

from app.core.config import (
    TARGET_SAMPLE_RATE,
    VAD_THRESHOLD,
    VAD_MIN_SPEECH_DURATION_MS,
    VAD_MIN_SILENCE_DURATION_MS,
)

# ======================================================
# LOAD VAD MODEL ONCE
# ======================================================

vad_model = load_silero_vad()

# ======================================================
# REMOVE SILENCE
# ======================================================

def remove_silence(waveform):

    """
    Removes non-speech regions.

    Returns:
        speech-only waveform
    """

    speech_timestamps = get_speech_timestamps(
        waveform.squeeze(),
        vad_model,
        sampling_rate=TARGET_SAMPLE_RATE,
        threshold=VAD_THRESHOLD,
        min_speech_duration_ms=VAD_MIN_SPEECH_DURATION_MS,
        min_silence_duration_ms=VAD_MIN_SILENCE_DURATION_MS,
    )

    # --------------------------------------------------
    # NO SPEECH DETECTED
    # --------------------------------------------------

    if len(speech_timestamps) == 0:
        return waveform

    # --------------------------------------------------
    # COLLECT SPEECH CHUNKS
    # --------------------------------------------------

    chunks = []

    for ts in speech_timestamps:

        start = ts["start"]
        end = ts["end"]

        chunks.append(
            waveform[:, start:end]
        )

    # --------------------------------------------------
    # CONCAT SPEECH CHUNKS
    # --------------------------------------------------

    cleaned_waveform = torch.cat(
        chunks,
        dim=1
    )

    return cleaned_waveform