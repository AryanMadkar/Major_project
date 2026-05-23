from pathlib import Path

# ======================================================
# BASE
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# ======================================================
# AUDIO
# ======================================================

TARGET_SAMPLE_RATE = 16000

# ======================================================
# WAVLM
# ======================================================

WAVLM_MODEL_NAME = "microsoft/wavlm-base-plus-sv"

USE_FP16 = True

WAVLM_THRESHOLD = 0.72

# ======================================================
# FILES
# ======================================================

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a"
}

MAX_FILE_SIZE_MB = 20

# ======================================================
# RATE LIMIT
# ======================================================

RATE_LIMIT_PER_MINUTE = 30