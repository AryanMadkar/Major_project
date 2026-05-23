import torchaudio
import torch

from app.core.config import TARGET_SAMPLE_RATE

# ======================================================
# LOAD AUDIO
# ======================================================

def load_audio(path):

    waveform, sample_rate = torchaudio.load(path)

    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    if sample_rate != TARGET_SAMPLE_RATE:

        resampler = torchaudio.transforms.Resample(
            orig_freq=sample_rate,
            new_freq=TARGET_SAMPLE_RATE,
        )

        waveform = resampler(waveform)

    return waveform
