import os
import warnings
import torch
import torch.nn.functional as F

warnings.filterwarnings("ignore")

from app.utils.hashing import get_file_hash
from app.audio.pipeline import process_audio
from app.models.embedding_cache import embedding_cache
from app.core.config import USE_FP16

# ======================================================
# DEVICE
# ======================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[XVECTOR] Device: {DEVICE}")

# ======================================================
# LOAD MODEL
# ======================================================

from speechbrain.inference.speaker import EncoderClassifier

print("[XVECTOR] Loading model...")

model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-resnet-voxceleb",
    savedir="pretrained_models/xvector",
    run_opts={
        "device": DEVICE
    }
)

model = model.to(DEVICE)

model.eval()

print("[XVECTOR] Model loaded!")

# ======================================================
# OPTIONAL FP16
# ======================================================

if DEVICE == "cuda" and USE_FP16:

    model = model.half()

    print("[XVECTOR] FP16 enabled")

# ======================================================
# WARMUP
# ======================================================

print("[XVECTOR] Warming up model...")

dummy = torch.randn(
    1,
    16000
).to(DEVICE)

if DEVICE == "cuda" and USE_FP16:
    dummy = dummy.half()

with torch.inference_mode():

    _ = model.encode_batch(dummy)

print("[XVECTOR] Warmup complete")

# ======================================================
# EMBEDDING EXTRACTION
# ======================================================

def get_embedding(audio_path):

    """
    Extract x-vector speaker embedding.
    """

    # --------------------------------------------------
    # HASH
    # --------------------------------------------------

    audio_hash = get_file_hash(audio_path)

    # --------------------------------------------------
    # CACHE HIT
    # --------------------------------------------------

    if audio_hash in embedding_cache:

        print("[CACHE] HIT")

        return embedding_cache[audio_hash]

    print("[CACHE] MISS")

    # --------------------------------------------------
    # PROCESS AUDIO
    # --------------------------------------------------

    waveform = process_audio(audio_path)

    # shape:
    # (1, samples)

    waveform = waveform.to(DEVICE)

    if DEVICE == "cuda" and USE_FP16:
        waveform = waveform.half()

    # --------------------------------------------------
    # INFERENCE
    # --------------------------------------------------

    with torch.inference_mode():

        embedding = model.encode_batch(
            waveform
        )

        embedding = F.normalize(
            embedding,
            p=2,
            dim=-1
        )

    embedding = embedding.squeeze()

    # --------------------------------------------------
    # CACHE
    # --------------------------------------------------

    embedding_cpu = embedding.detach().float().cpu()

    embedding_cache[audio_hash] = embedding_cpu

    return embedding_cpu