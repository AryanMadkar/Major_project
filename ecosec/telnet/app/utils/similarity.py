import torch

# ======================================================
# COSINE SIMILARITY
# ======================================================

def cosine_similarity(emb1, emb2):

    # --------------------------------------------------
    # ENSURE 1D VECTORS
    # --------------------------------------------------

    if emb1.dim() > 1:
        emb1 = emb1.squeeze()
    if emb2.dim() > 1:
        emb2 = emb2.squeeze()

    # --------------------------------------------------
    # VERIFY SAME DIMENSION
    # --------------------------------------------------

    if emb1.shape != emb2.shape:
        raise ValueError(
            f"Embedding shape mismatch: "
            f"{emb1.shape} vs {emb2.shape}"
        )

    # --------------------------------------------------
    # DOT PRODUCT (assuming normalized vectors)
    # --------------------------------------------------

    similarity = torch.dot(
        emb1.float(),
        emb2.float()
    ).item()

    return similarity