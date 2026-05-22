import torch

# ======================================================
# COSINE SIMILARITY
# ======================================================

def cosine_similarity(emb1, emb2):

    similarity = torch.dot(
        emb1,
        emb2
    ).item()

    return similarity