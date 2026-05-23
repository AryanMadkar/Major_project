import torch

from silero_vad import get_speech_timestamps, load_silero_vad

from app.core.config import TARGET_SAMPLE_RATE

vad_model = load_silero_vad()

# ======================================================
# REMOVE SILENCE
# ======================================================

def remove_silence(waveform):

    speech_timestamps = get_speech_timestamps(
        waveform.squeeze(),
        vad_model,
        sampling_rate=TARGET_SAMPLE_RATE,
    )

    if len(speech_timestamps) == 0:
        raise ValueError("No speech detected in audio.")

    speech_segments = []

    for segment in speech_timestamps:

        start = segment["start"]
        end = segment["end"]

        speech_segments.append(waveform[:, start:end])

    return torch.cat(speech_segments, dim=1)
