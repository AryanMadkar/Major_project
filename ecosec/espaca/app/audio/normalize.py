import torch

# ======================================================
# NORMALIZE AUDIO
# ======================================================

def normalize_audio(waveform):

    """
    Peak normalize audio.

    Keeps waveform in stable range.
    """

    peak = waveform.abs().max()

    if peak > 0:
        waveform = waveform / peak

    return waveform