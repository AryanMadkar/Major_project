import os
import warnings
import torch
import torch.nn.functional as F

warnings.filterwarnings("ignore")

from app.core.config import (
    NEMO_CACHE_DIR,
    TARGET_SAMPLE_RATE
)

from app.utils.hashing import get_file_hash
from app.audio.pipeline import process_audio
from app.models.embedding_cache import embedding_cache

# ======================================================
# DEVICE
# ======================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[TITANET] Device: {DEVICE}")

# ======================================================
# LOAD MODEL
# ======================================================

os.environ.setdefault(
    "NEMO_CACHE_DIR",
    str(NEMO_CACHE_DIR)
)
os.environ.setdefault(
    "NEMO_HOME",
    str(NEMO_CACHE_DIR)
)

from nemo.collections.asr.models import EncDecSpeakerLabelModel

print("[TITANET] Loading model...")

model = EncDecSpeakerLabelModel.from_pretrained(
    model_name="titanet_large"
)

model = model.to(DEVICE)

model.eval()

print("[TITANET] Model loaded!")

# ======================================================
# OPTIONAL FP16
# ======================================================

if DEVICE == "cuda":

    model = model.half()

    print("[TITANET] FP16 enabled")

# ======================================================
# MODEL WARMUP
# ======================================================

print("[TITANET] Warming up model...")

dummy = torch.randn(
    1,
    TARGET_SAMPLE_RATE
).to(DEVICE)

if DEVICE == "cuda":
    dummy = dummy.half()

with torch.inference_mode():

    _ = model.forward(
        input_signal=dummy,
        input_signal_length=torch.tensor([TARGET_SAMPLE_RATE]).to(DEVICE)
    )

print("[TITANET] Warmup complete")

# ======================================================
# EMBEDDING EXTRACTION
# ======================================================

def get_embedding(audio_path):

    """
    Extract speaker embedding with cache optimization.
    """

    # --------------------------------------------------
    # HASH AUDIO
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

    # waveform shape:
    # (1, samples)

    waveform = waveform.to(DEVICE)

    if DEVICE == "cuda":
        waveform = waveform.half()

    # length tensor
    length = torch.tensor(
        [waveform.shape[1]]
    ).to(DEVICE)

    # --------------------------------------------------
    # INFERENCE
    # --------------------------------------------------

    with torch.inference_mode():

        _, embedding = model.forward(
            input_signal=waveform,
            input_signal_length=length
        )

        # normalize embedding
        embedding = F.normalize(
            embedding,
            p=2,
            dim=-1
        )

    embedding = embedding.squeeze()

    embedding_cpu = embedding.detach().float().cpu()

    # --------------------------------------------------
    # CACHE
    # --------------------------------------------------

    embedding_cache[audio_hash] = embedding_cpu

    return embedding_cpu