from concurrent.futures import ThreadPoolExecutor
from app.core.config import SPEAKER_THRESHOLD
from app.models.deepspeaker import get_embedding
from app.utils.similarity import cosine_similarity
from app.core.logger import logger

# ======================================================
# VERIFY
# ======================================================

def verify_speaker(audio1, audio2):

    logger.info("[VERIFICATION] Extracting embeddings concurrently")
    logger.info("[DUAL] Starting concurrent embedding extraction")
    logger.info("[THREADING] Starting with 2 workers")

    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(get_embedding, audio1)
        future2 = executor.submit(get_embedding, audio2)

        emb1 = future1.result()
        emb2 = future2.result()

    similarity = cosine_similarity(emb1, emb2)

    same_speaker = similarity >= SPEAKER_THRESHOLD

    return {
        "model": "deepspeaker",
        "similarity": round(similarity, 4),
        "threshold": SPEAKER_THRESHOLD,
        "same_speaker": same_speaker,
    }

