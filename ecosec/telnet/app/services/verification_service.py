from app.models.telnet import get_embedding
from app.utils.similarity import cosine_similarity
from app.core.config import SPEAKER_THRESHOLD
from app.core.logger import logger

# ======================================================
# VERIFY
# ======================================================

def verify_speaker(audio1, audio2):

    # --------------------------------------------------
    # EXTRACT EMBEDDINGS (sequential – PyTorch model
    # inference is NOT thread-safe on CPU)
    # --------------------------------------------------

    logger.info("[VERIFICATION] Extracting embeddings")

    emb1 = get_embedding(audio1)
    emb2 = get_embedding(audio2)

    logger.info("[VERIFICATION] Embedding extraction complete")

    # --------------------------------------------------
    # SIMILARITY
    # --------------------------------------------------

    similarity = cosine_similarity(
        emb1,
        emb2
    )

    # --------------------------------------------------
    # DECISION
    # --------------------------------------------------

    same_speaker = similarity >= SPEAKER_THRESHOLD

    return {

        "model": "telnet",

        "similarity": round(similarity, 4),

        "threshold": SPEAKER_THRESHOLD,

        "same_speaker": same_speaker
    }