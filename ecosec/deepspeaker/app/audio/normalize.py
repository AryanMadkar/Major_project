import torch

# ======================================================
# NORMALIZE AUDIO
# ======================================================

def normalize_audio(waveform):

    peak = waveform.abs().max()

    if peak > 0:
        waveform = waveform / peak

    return waveform
