from app.models.wavlm import get_embedding

from app.utils.similarity import cosine_similarity

from app.core.config import WAVLM_THRESHOLD

# ======================================================
# VERIFY
# ======================================================

def verify_wavlm(audio1, audio2):

    emb1 = get_embedding(audio1)

    emb2 = get_embedding(audio2)

    similarity = cosine_similarity(
        emb1,
        emb2
    )

    same_speaker = similarity >= WAVLM_THRESHOLD

    return {

        "model": "wavlm",

        "similarity": round(similarity, 4),

        "same_speaker": same_speaker,
        
        "threshold": WAVLM_THRESHOLD

    }