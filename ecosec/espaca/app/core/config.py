from pathlib import Path

# ======================================================
# BASE DIRECTORIES
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

TEMP_DIR = BASE_DIR / "temp"

# create temp folder automatically
TEMP_DIR.mkdir(exist_ok=True)

# ======================================================
# AUDIO SETTINGS
# ======================================================

TARGET_SAMPLE_RATE = 16000

# ======================================================
# ECAPA SETTINGS
# ======================================================

ECAPA_MODEL_NAME = "speechbrain/spkrec-ecapa-voxceleb"

# ======================================================
# SERVER SETTINGS
# ======================================================

MAX_FILE_SIZE_MB = 20