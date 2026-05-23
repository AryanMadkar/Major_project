from pathlib import Path
import os

# ======================================================
# BASE
# ======================================================

BASE_DIR = Path(__file__).resolve().parent

# ======================================================
# FILES
# ======================================================

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".flac",
    ".ogg",
    ".m4a",
}

MAX_FILE_SIZE_MB = 20

# ======================================================
# MODEL ENDPOINTS
# ======================================================

MODEL_ENDPOINTS = [
    {
        "name": "espaca",
        "url": os.getenv("ESPACA_VERIFY_URL", "http://127.0.0.1:8000/verify"),
        "weight": float(os.getenv("ESPACA_MODEL_WEIGHT", "0.30")),
    },
    {
        "name": "resnet",
        "url": os.getenv("RESNET_VERIFY_URL", "http://127.0.0.1:8001/verify"),
        "weight": float(os.getenv("RESNET_MODEL_WEIGHT", "0.25")),
    },
    {
        "name": "telnet",
        "url": os.getenv("TELNET_VERIFY_URL", "http://127.0.0.1:8002/verify"),
        "weight": float(os.getenv("TELNET_MODEL_WEIGHT", "0.20")),
    },
    {
        "name": "wavlm",
        "url": os.getenv("WAVLM_VERIFY_URL", "http://127.0.0.1:8003/verify"),
        "weight": float(os.getenv("WAVLM_MODEL_WEIGHT", "0.25")),
    },
     {
        "name": "deepspeaker",
        "url": os.getenv("DEEPSPEAKER_VERIFY_URL", "http://127.0.0.1:8006/verify"),
        "weight": float(os.getenv("DEEPSPEAKER_MODEL_WEIGHT", "0.25")),
    },
]

AGGREGATION_THRESHOLD = float(os.getenv("ORCHESTRATION_THRESHOLD", "0.5"))
REQUEST_TIMEOUT_SECONDS = float(os.getenv("MODEL_REQUEST_TIMEOUT", "120"))
ORCHESTRATION_PORT = int(os.getenv("ORCHESTRATION_PORT", "8010"))
