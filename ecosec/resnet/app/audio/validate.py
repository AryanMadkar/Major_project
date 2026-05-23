# ======================================================
# VALIDATE SPEECH LENGTH
# ======================================================

from app.core.config import TARGET_SAMPLE_RATE

MIN_AUDIO_SECONDS = 1.0

def validate_audio(waveform):

    """
    Ensures audio contains enough speech.
    """

    duration = waveform.shape[1] / TARGET_SAMPLE_RATE

    if duration < MIN_AUDIO_SECONDS:

        raise ValueError(
            f"Audio too short: {duration:.2f}s"
        )

    return True