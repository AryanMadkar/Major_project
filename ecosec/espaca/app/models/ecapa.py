import torch
import torch.nn.functional as F

from speechbrain.inference import EncoderClassifier

from app.audio.pipeline import process_audio

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

    source="speechbrain/spkrec-ecapa-voxceleb",

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
    16000
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
    Extract speaker embedding.
    """

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

    return embedding