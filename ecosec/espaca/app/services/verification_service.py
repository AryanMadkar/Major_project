from app.models.ecapa import get_embedding
from app.utils.similarity import cosine_similarity


# ======================================================
# THRESHOLD
# ======================================================

THRESHOLD = 0.72

# ======================================================
# VERIFY
# ======================================================

def verify_speaker(audio1, audio2):

    # --------------------------------------------------
    # GET EMBEDDINGS
    # --------------------------------------------------

    emb1 = get_embedding(audio1)

    emb2 = get_embedding(audio2)

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

    same_speaker = similarity >= THRESHOLD

    return {

        "similarity": round(similarity, 4),

        "threshold": THRESHOLD,

        "same_speaker": same_speaker
    }