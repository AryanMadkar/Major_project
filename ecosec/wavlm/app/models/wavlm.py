import warnings

import torch
import torch.nn.functional as F

from transformers import (
    WavLMForXVector,
    AutoFeatureExtractor
)

from app.audio.pipeline import process_audio

from app.utils.hashing import get_file_hash

from app.models.embedding_cache import (
    embedding_cache
)

from app.core.config import (
    WAVLM_MODEL_NAME,
    USE_FP16,
    TARGET_SAMPLE_RATE
)

# ======================================================
# WARNINGS
# ======================================================

warnings.filterwarnings("ignore")

# ======================================================
# GPU OPTIMIZATION
# ======================================================

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

torch.set_float32_matmul_precision("high")

# ======================================================
# DEVICE
# ======================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[WAVLM] Device: {DEVICE}")

# ======================================================
# LOAD FEATURE EXTRACTOR
# ======================================================

print("[WAVLM] Loading feature extractor...")

feature_extractor = AutoFeatureExtractor.from_pretrained(
    WAVLM_MODEL_NAME
)

# ======================================================
# LOAD MODEL
# ======================================================

print("[WAVLM] Loading model...")

model = WavLMForXVector.from_pretrained(
    WAVLM_MODEL_NAME
)

model = model.to(DEVICE)

model.eval()

print("[WAVLM] Model loaded!")

# ======================================================
# FP16
# ======================================================

if DEVICE == "cuda" and USE_FP16:

    model = model.half()

    print("[WAVLM] FP16 enabled")

# ======================================================
# WARMUP
# ======================================================

print("[WAVLM] Warming up model...")

dummy = torch.randn(
    1,
    TARGET_SAMPLE_RATE
).to(DEVICE)

if DEVICE == "cuda" and USE_FP16:
    dummy = dummy.half()

with torch.inference_mode():

    warmup_outputs = model(dummy)

    _ = (
        warmup_outputs.embeddings
        if getattr(warmup_outputs, "embeddings", None) is not None
        else warmup_outputs.last_hidden_state
    )

print("[WAVLM] Warmup complete")

# ======================================================
# GET EMBEDDING
# ======================================================

def get_embedding(audio_path):

    # --------------------------------------------------
    # HASH
    # --------------------------------------------------

    audio_hash = get_file_hash(audio_path)

    # --------------------------------------------------
    # CACHE
    # --------------------------------------------------

    if audio_hash in embedding_cache:

        print("[CACHE] HIT")

        return embedding_cache[audio_hash]

    print("[CACHE] MISS")

    # --------------------------------------------------
    # PROCESS AUDIO
    # --------------------------------------------------

    waveform = process_audio(audio_path)

    waveform = waveform.squeeze(0)

    # --------------------------------------------------
    # FEATURE EXTRACTION
    # --------------------------------------------------

    inputs = feature_extractor(
        waveform.cpu().numpy(),
        sampling_rate=TARGET_SAMPLE_RATE,
        return_tensors="pt"
    )

    input_values = inputs.input_values.to(DEVICE)

    if DEVICE == "cuda" and USE_FP16:

        input_values = input_values.half()

    # --------------------------------------------------
    # INFERENCE
    # --------------------------------------------------

    with torch.inference_mode():

        outputs = model(input_values)

        embeddings = getattr(outputs, "embeddings", None)

        if embeddings is None:

            hidden_states = outputs.last_hidden_state

            embeddings = hidden_states.mean(dim=1)

        embedding = F.normalize(
            embeddings,
            p=2,
            dim=-1
        )

    embedding = embedding.squeeze()

    embedding_cpu = embedding.detach().float().cpu()

    # --------------------------------------------------
    # CACHE SAVE
    # --------------------------------------------------

    embedding_cache[audio_hash] = embedding_cpu

    return embedding_cpu