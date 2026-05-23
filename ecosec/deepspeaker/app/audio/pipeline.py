from app.audio.loader import load_audio
from app.audio.normalize import normalize_audio
from app.audio.vad import remove_silence
from app.audio.validate import validate_audio
from app.utils.timers import Timer

# ======================================================
# AUDIO PIPELINE
# ======================================================

def process_audio(path):

    with Timer("audio_pipeline"):

        waveform = load_audio(path)
        waveform = remove_silence(waveform)
        waveform = normalize_audio(waveform)
        validate_audio(waveform)

        return waveform
