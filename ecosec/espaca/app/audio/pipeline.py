from app.audio.loader import load_audio
from app.utils.timers import Timer

# ======================================================
# AUDIO PIPELINE
# ======================================================

def process_audio(path):

    with Timer("audio_pipeline"):

        waveform = load_audio(path)

        return waveform