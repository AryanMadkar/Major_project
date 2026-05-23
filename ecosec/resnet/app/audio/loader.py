import torchaudio
import torch

from app.core.config import TARGET_SAMPLE_RATE

# ======================================================
# LOAD AUDIO
# ======================================================

def load_audio(path):

    """
    Loads audio safely and converts it into:
    
    - mono
    - float32
    - 16kHz

    Returns:
        waveform: Tensor [1, samples]
    """

    try:

        # --------------------------------------------------
        # LOAD AUDIO
        # --------------------------------------------------

        waveform, sample_rate = torchaudio.load(path)

        # --------------------------------------------------
        # VALIDATE
        # --------------------------------------------------

        if waveform.numel() == 0:
            raise ValueError("Empty audio file")

        # --------------------------------------------------
        # CONVERT TO MONO
        # --------------------------------------------------

        if waveform.shape[0] > 1:

            waveform = torch.mean(
                waveform,
                dim=0,
                keepdim=True
            )

        # --------------------------------------------------
        # RESAMPLE
        # --------------------------------------------------

        if sample_rate != TARGET_SAMPLE_RATE:

            waveform = torchaudio.functional.resample(
                waveform,
                sample_rate,
                TARGET_SAMPLE_RATE
            )

        # --------------------------------------------------
        # NORMALIZE DTYPE
        # --------------------------------------------------

        waveform = waveform.float()

        return waveform

    except Exception as e:

        raise RuntimeError(
            f"Audio loading failed: {str(e)}"
        )