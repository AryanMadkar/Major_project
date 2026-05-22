# =====================================================
# config.py — Central thresholds for all speaker
# verification models. Tune these values based on
# your dataset / False-Acceptance vs False-Rejection
# trade-off requirements.
# =====================================================

# ECAPA-TDNN model threshold.
# Cosine similarity must be >= this value to be
# considered the SAME speaker.
# Range: 0.0 – 1.0 (higher = stricter matching)
ECAPA_THRESHOLD = 0.70

# TitaNet-Large model threshold.
# NeMo embeddings tend to cluster slightly differently,
# so this is tuned a bit lower.
TITANET_THRESHOLD = 0.60

# "Optimized" (ensemble-refined) ECAPA model threshold.
# Kept lower because audio goes through VAD preprocessing
# which changes the signal characteristics slightly.
OPTIMIZED_THRESHOLD = 0.68

# =====================================================
# Directory where SpeechBrain / NeMo will cache
# pre-trained model weights.
# Use a relative path so this works on any machine.
# =====================================================
import os

# Root directory of the project (one level up from app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All downloaded model weights go here
PRETRAINED_MODELS_DIR = os.path.join(BASE_DIR, "pretrained_models")

# Per-model subdirectories
ECAPA_MODEL_DIR      = os.path.join(PRETRAINED_MODELS_DIR, "ecapa")
TITANET_MODEL_DIR    = os.path.join(PRETRAINED_MODELS_DIR, "titanet")
OPTIMIZED_MODEL_DIR  = os.path.join(PRETRAINED_MODELS_DIR, "optimized")