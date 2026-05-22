# =====================================================
# agents/ecapa_agent.py
#
# Speaker verification using SpeechBrain's
# ECAPA-TDNN model trained on VoxCeleb.
#
# ECAPA-TDNN (Emphasized Channel Attention, Propagation
# and Aggregation in TDNN) produces 192-dim speaker
# embeddings. Cosine similarity between two embeddings
# is used to decide same vs different speaker.
# =====================================================

import torch
import torch.nn.functional as F
import librosa

# SpeechBrain's high-level inference wrapper.
# It handles loading the YAML recipe + weights automatically.
from speechbrain.inference import EncoderClassifier

# Centralised config — thresholds and model paths live here
from ..config import ECAPA_THRESHOLD, ECAPA_MODEL_DIR


# ── Device setup ────────────────────────────────────
# Use GPU when available for faster embedding extraction.
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# ── Model loading ────────────────────────────────────
# This runs ONCE when the module is first imported
# (i.e. at server startup), not on every request.
# `savedir` is a LOCAL cache folder where SpeechBrain
# will download & store the pretrained weights the
# first time; subsequent starts load from disk.
model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",  # HuggingFace model ID
    savedir=ECAPA_MODEL_DIR,                      # portable local cache path
    run_opts={"device": DEVICE}                  # tell SpeechBrain which device to use
)

model.eval()   # switch to inference mode (disables dropout etc.)


# ── Audio loading ────────────────────────────────────

def load_audio(audio_path: str) -> torch.Tensor:
    """
    Load a WAV file with librosa and return a
    (1, samples) float32 tensor on DEVICE.

    We use librosa here (instead of torchaudio) because
    SpeechBrain's encode_batch expects the raw signal
    tensor in a specific shape, and librosa gives us
    consistent resampling behaviour across platforms.
    """

    # librosa.load always returns mono float32 at the requested sr
    signal, _sr = librosa.load(
        audio_path,
        sr=16_000,    # must match model training sample rate
        mono=True     # collapse any stereo to mono
    )

    # librosa returns a 1-D numpy array; SpeechBrain wants (batch, samples)
    signal = torch.tensor(signal).unsqueeze(0)  # shape: (1, samples)

    return signal.to(DEVICE)


# ── Embedding extraction ─────────────────────────────

def get_embedding(audio_path: str) -> torch.Tensor:
    """
    Run the ECAPA-TDNN encoder and return a
    L2-normalised 1-D embedding vector.

    L2 normalisation makes cosine similarity equivalent
    to a plain dot product, which is faster.
    """

    signal = load_audio(audio_path)

    with torch.no_grad():   # no gradients needed at inference time
        # encode_batch returns shape (batch, 1, embedding_dim)
        embedding = model.encode_batch(signal)

        # Normalise to unit length along the last dimension
        embedding = F.normalize(embedding, p=2, dim=-1)

    # Remove batch and extra dims → 1-D vector of shape (embedding_dim,)
    return embedding.squeeze()


# ── Verification ─────────────────────────────────────

def verify(audio1: str, audio2: str) -> dict:
    """
    Compare two audio files and return a result dict.

    Returns:
        {
            "model":        "ecapa",
            "score":        float,   # cosine similarity in [-1, 1]
            "same_speaker": bool     # True if score >= ECAPA_THRESHOLD
        }
    """

    emb1 = get_embedding(audio1)
    emb2 = get_embedding(audio2)

    # Dot product of unit vectors == cosine similarity
    similarity = torch.dot(emb1, emb2).item()

    return {
        "model":        "ecapa",
        "score":        round(similarity, 4),
        "same_speaker": similarity >= ECAPA_THRESHOLD
    }