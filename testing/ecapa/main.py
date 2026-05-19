import os
import torch
import torch.nn.functional as F

from functools import lru_cache
from speechbrain.pretrained import SpeakerRecognition

# =====================================================
# CONFIG
# =====================================================

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Using device: {DEVICE}")

# =====================================================
# LOAD MODEL ONCE
# =====================================================

verification_model = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="./pretrained_models",
    run_opts={"device": DEVICE},
)

# =====================================================
# CACHED EMBEDDING EXTRACTION
# =====================================================

@lru_cache(maxsize=1000)
def get_embedding(audio_path: str):
    """
    Load audio, extract embedding, squeeze to [192],
    and L2-normalize — all inside the cache so every
    lookup returns a ready-to-use flat vector.
    """
    with torch.inference_mode():
        signal = verification_model.load_audio(audio_path)
        signal = signal.unsqueeze(0).to(DEVICE)
        embedding = verification_model.encode_batch(signal)  # [1, 1, 192]

    embedding = embedding.squeeze()                          # [192]
    embedding = F.normalize(embedding, p=2, dim=0)          # unit vector
    return embedding


# =====================================================
# VERIFY USING EMBEDDINGS
# =====================================================

def verify_speakers(
    audio1_path: str,
    audio2_path: str,
    threshold: float = 0.25   # calibrated for ECAPA cosine score range
):
    """
    Verify whether two audio files belong to the same speaker.

    Args:
        audio1_path (str): Path to first audio file
        audio2_path (str): Path to second audio file
        threshold (float): Cosine similarity threshold (default: 0.25)

    Returns:
        dict: Verification result with score and prediction
    """
    try:
        # Get cached, normalized flat embeddings [192]
        emb1 = get_embedding(audio1_path)
        emb2 = get_embedding(audio2_path)

        # Dot product of two unit vectors = cosine similarity
        similarity = torch.dot(emb1, emb2).item()

        return {
            "success": True,
            "similarity_score": round(similarity, 4),
            "same_speaker": similarity >= threshold,
            "threshold": threshold,
            "device": DEVICE,
            "audio_1": audio1_path,
            "audio_2": audio2_path,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "same_speaker": False,
        }


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    result = verify_speakers(
        r"D:\majorproject\testing\ecapa\audio-dataset\aryan2.mp3",
        r"D:\majorproject\testing\ecapa\audio-dataset\Aryan.mp3"
    )

    print(result)