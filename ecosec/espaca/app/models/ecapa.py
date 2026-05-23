import torch
torch.set_num_threads(2)
import torch.nn.functional as F

# warnings.filterwarnings(
#     "ignore",
#     message=r"`torch\.cuda\.amp\.custom_fwd.*",
#     category=FutureWarning,
# )
# warnings.filterwarnings(
#     "ignore",
#     message=r"Requested Pretrainer collection using symlinks on Windows.*",
#     category=UserWarning,
# )
# warnings.filterwarnings(
#     "ignore",
#     message=r"Module 'speechbrain\.pretrained' was deprecated.*",
#     category=UserWarning,
# )

from speechbrain.inference import EncoderClassifier
from app.utils.hashing import get_file_hash
from app.audio.pipeline import process_audio
from app.models.embedding_cache import embedding_cache
from app.core.config import (
    ECAPA_MODEL_NAME,
    TARGET_SAMPLE_RATE
)
# ======================================================
# DEVICE
# ======================================================


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[ECAPA] Device: {DEVICE}")

# ======================================================
# LOAD MODEL
# ======================================================

print("[ECAPA] Loading model...")

model = EncoderClassifier.from_hparams(

    source=ECAPA_MODEL_NAME,

    savedir="cache/ecapa",

    run_opts={
        "device": DEVICE
    }
)

# inference mode
model.eval()

print("[ECAPA] Model loaded!")

# ======================================================
# OPTIONAL FP16
# ======================================================

if DEVICE == "cuda":

    model = model.half()

    print("[ECAPA] FP16 enabled")

# ======================================================
# MODEL WARMUP
# ======================================================

print("[ECAPA] Warming up model...")

dummy = torch.randn(
    1,
    TARGET_SAMPLE_RATE
).to(DEVICE)

if DEVICE == "cuda":
    dummy = dummy.half()

with torch.inference_mode():

    _ = model.encode_batch(dummy)

print("[ECAPA] Warmup complete")

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

    # --------------------------------------------------
    # MOVE TO DEVICE
    # --------------------------------------------------

    waveform = waveform.to(DEVICE)

    # --------------------------------------------------
    # FP16
    # --------------------------------------------------

    if DEVICE == "cuda":
        waveform = waveform.half()

    # --------------------------------------------------
    # INFERENCE
    # --------------------------------------------------

    with torch.inference_mode():

        embedding = model.encode_batch(
            waveform
        )

        # normalize embedding
        embedding = F.normalize(
            embedding,
            p=2,
            dim=-1
        )

    # (1,1,192) -> (192,)
    embedding = embedding.squeeze()

    embedding_cpu = embedding.detach().float().cpu()

    # Cache the embedding
    embedding_cache[audio_hash] = embedding_cpu

    return embedding_cpu