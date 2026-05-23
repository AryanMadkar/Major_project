import torch
torch.set_num_threads(2)
import torch.nn.functional as F

# warnings.filterwarnings("ignore")

from speechbrain.inference import EncoderClassifier

from app.audio.pipeline import process_audio
from app.core.config import DEEPSPEAKER_MODEL_NAME, TARGET_SAMPLE_RATE
from app.models.embedding_cache import embedding_cache
from app.utils.hashing import get_file_hash

# ======================================================
# DEVICE
# ======================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[DEEPSPEAKER] Device: {DEVICE}")

# ======================================================
# LOAD MODEL
# ======================================================

print("[DEEPSPEAKER] Loading model...")

model = EncoderClassifier.from_hparams(
    source=DEEPSPEAKER_MODEL_NAME,
    savedir="cache/deepspeaker",
    run_opts={"device": DEVICE},
)

model.eval()

print("[DEEPSPEAKER] Model loaded!")

if DEVICE == "cuda":
    model = model.half()
    print("[DEEPSPEAKER] FP16 enabled")

print("[DEEPSPEAKER] Warming up model...")

dummy = torch.randn(1, TARGET_SAMPLE_RATE).to(DEVICE)

if DEVICE == "cuda":
    dummy = dummy.half()

with torch.inference_mode():
    _ = model.encode_batch(dummy)

print("[DEEPSPEAKER] Warmup complete")

# ======================================================
# EMBEDDING EXTRACTION
# ======================================================

def get_embedding(audio_path):

    audio_hash = get_file_hash(audio_path)

    if audio_hash in embedding_cache:
        print("[CACHE] HIT")
        return embedding_cache[audio_hash]

    print("[CACHE] MISS")

    waveform = process_audio(audio_path)
    waveform = waveform.to(DEVICE)

    if DEVICE == "cuda":
        waveform = waveform.half()

    with torch.inference_mode():
        embedding = model.encode_batch(waveform)
        embedding = F.normalize(embedding, p=2, dim=-1)

    embedding = embedding.squeeze()
    embedding_cpu = embedding.detach().float().cpu()
    embedding_cache[audio_hash] = embedding_cpu

    return embedding_cpu
