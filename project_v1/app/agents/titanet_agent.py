# =====================================================
# agents/titanet_agent.py
#
# Speaker verification using NVIDIA NeMo's
# TitaNet-Large model.
#
# TitaNet uses a SqueezeExcitation + 1-D convolution
# architecture and produces 192-dim embeddings.
# It's trained on a large mix of VoxCeleb, LibriSpeech
# and internal NVIDIA data.
# =====================================================

import torch
import torch.nn.functional as F

# NeMo's ASR collection contains the speaker label model
from nemo.collections.asr.models import EncDecSpeakerLabelModel

# Centralised config
from ..config import TITANET_THRESHOLD


# ── Device setup ────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ── Model loading ────────────────────────────────────
# NeMo downloads the weights from NGC on first run
# and caches them in ~/.cache/torch/NeMo by default.
# `from_pretrained` accepts the NGC model card name.
model = EncDecSpeakerLabelModel.from_pretrained(
    model_name="titanet_large"
)

model = model.to(DEVICE)
model.eval()   # inference mode — disables training-only ops like dropout


# ── Embedding extraction ─────────────────────────────

def get_embedding(audio_path: str) -> torch.Tensor:
    """
    Run TitaNet-Large on a WAV file and return a
    L2-normalised embedding vector.

    NeMo's get_embedding() handles its own audio loading
    internally (resampling, feature extraction etc.),
    so we only need to pass the file path.
    """

    with torch.no_grad():   # disable autograd for speed & memory
        # Returns shape (1, embedding_dim)
        embedding = model.get_embedding(audio_path)

        # L2-normalise so dot product == cosine similarity
        embedding = F.normalize(embedding, p=2, dim=-1)

    # Squeeze to 1-D vector (embedding_dim,)
    return embedding.squeeze()


# ── Verification ─────────────────────────────────────

def verify(audio1: str, audio2: str) -> dict:
    """
    Compare two audio files with TitaNet-Large.

    Returns:
        {
            "model":        "titanet",
            "score":        float,   # cosine similarity
            "same_speaker": bool
        }
    """

    emb1 = get_embedding(audio1)
    emb2 = get_embedding(audio2)

    # Cosine similarity via dot product of unit vectors
    similarity = torch.dot(emb1, emb2).item()

    return {
        "model":        "titanet",
        "score":        round(similarity, 4),
        "same_speaker": similarity >= TITANET_THRESHOLD
    }