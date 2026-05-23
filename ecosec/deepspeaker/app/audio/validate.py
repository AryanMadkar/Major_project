from app.core.config import TARGET_SAMPLE_RATE

MIN_AUDIO_SECONDS = 1.0

# ======================================================
# VALIDATE AUDIO
# ======================================================

def validate_audio(waveform):

    duration = waveform.shape[1] / TARGET_SAMPLE_RATE

    if duration < MIN_AUDIO_SECONDS:
        raise ValueError(f"Audio too short: {duration:.2f}s")

    return True
