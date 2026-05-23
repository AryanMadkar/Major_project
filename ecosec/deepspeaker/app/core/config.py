from pathlib import Path

# ======================================================
# BASE DIRECTORIES
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ======================================================
# AUDIO SETTINGS
# ======================================================

TARGET_SAMPLE_RATE = 16000

# ======================================================
# DEEPSPEAKER SETTINGS
# ======================================================

DEEPSPEAKER_MODEL_NAME = "speechbrain/spkrec-resnet-voxceleb"

# ======================================================
# VERIFICATION SETTINGS
# ======================================================

SPEAKER_THRESHOLD = 0.62

# ======================================================
# SERVER SETTINGS
# ======================================================

RATE_LIMIT_PER_MINUTE = 30

# ======================================================
# FILE VALIDATION
# ======================================================

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a",
}

MAX_FILE_SIZE_MB = 20
