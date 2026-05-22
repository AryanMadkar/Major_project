# ======================================================
# VALIDATE SPEECH LENGTH
# ======================================================

MIN_AUDIO_SECONDS = 1.0

TARGET_SR = 16000

def validate_audio(waveform):

    """
    Ensures audio contains enough speech.
    """

    duration = waveform.shape[1] / TARGET_SR

    if duration < MIN_AUDIO_SECONDS:

        raise ValueError(
            f"Audio too short: {duration:.2f}s"
        )

    return True