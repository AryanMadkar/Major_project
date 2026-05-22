# =====================================================
# agents/optimized_agent.py
#
# A "fine-tuned" variant of the ECAPA-TDNN pipeline.
# The key difference from ecapa_agent.py is:
#
#   1. Uses OPTIMIZED_THRESHOLD (tuned separately)
#   2. Uses the OPTIMIZED_MODEL_DIR cache folder, so
#      you can later swap in a fine-tuned checkpoint
#      without touching ecapa_agent.py
#   3. Designed to receive audio that has ALREADY been
#      VAD-preprocessed by audio.py (optimised files),
#      so it skips its own preprocessing.
# =====================================================

import torch
import torch.nn.functional as F
import librosa

from speechbrain.inference import EncoderClassifier

# Import the correct threshold and model directory for THIS agent
from ..config import OPTIMIZED_THRESHOLD, OPTIMIZED_MODEL_DIR


# ── Device setup ────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[optimized_agent] Using device: {DEVICE}")


# ── Model loading ────────────────────────────────────
# By pointing savedir to OPTIMIZED_MODEL_DIR you can
# later drop a fine-tuned checkpoint there and this
# agent will pick it up without changing ecapa_agent.
print("[optimized_agent] Loading model...")

model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",   # base pretrained weights
    savedir=OPTIMIZED_MODEL_DIR,                   # separate local cache
    run_opts={"device": DEVICE}
)

model.eval()   # inference mode

print("[optimized_agent] Model loaded!")


# ── Audio loading ────────────────────────────────────

def load_audio(audio_path: str) -> torch.Tensor:
    """
    Load audio into a (1, samples) tensor.
    Assumes the file has already been resampled to
    16 kHz and had silence stripped by audio.py.
    """

    # librosa gives consistent float32 output across platforms
    signal, _sr = librosa.load(
        audio_path,
        sr=16_000,
        mono=True
    )

    # Add batch dimension: (samples,) → (1, samples)
    return torch.tensor(signal).unsqueeze(0).to(DEVICE)


# ── Embedding extraction ─────────────────────────────

def get_embedding(audio_path: str) -> torch.Tensor:
    """
    Extract and L2-normalise an ECAPA-TDNN embedding.
    """

    signal = load_audio(audio_path)

    with torch.no_grad():
        # encode_batch: (1, samples) → (1, 1, embedding_dim)
        embedding = model.encode_batch(signal)
        # Normalise so dot product == cosine similarity
        embedding = F.normalize(embedding, p=2, dim=-1)

    # (1, 1, dim) → (dim,)
    return embedding.squeeze()


# ── Verification ─────────────────────────────────────

def verify(audio1: str, audio2: str) -> dict:
    """
    Compare two preprocessed audio files.

    Note: uses OPTIMIZED_THRESHOLD, NOT the ECAPA one.
    This is the main behavioural difference from ecapa_agent.

    Returns:
        {
            "model":        "optimized",
            "score":        float,
            "same_speaker": bool
        }
    """

    print("[optimized_agent] Extracting embeddings...")

    emb1 = get_embedding(audio1)
    emb2 = get_embedding(audio2)

    # Cosine similarity
    similarity = torch.dot(emb1, emb2).item()

    print(f"[optimized_agent] Similarity Score: {similarity:.4f}")
    print(f"[optimized_agent] Threshold: {OPTIMIZED_THRESHOLD}")
    print(f"[optimized_agent] Decision: {'Same Speaker' if similarity >= OPTIMIZED_THRESHOLD else 'Different Speaker'}")

    return {
        "model":        "optimized",
        "score":        round(similarity, 4),
        # BUG FIX: was hardcoded to 0.70; now correctly uses OPTIMIZED_THRESHOLD
        "same_speaker": similarity >= OPTIMIZED_THRESHOLD
    }