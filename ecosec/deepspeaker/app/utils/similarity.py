import torch

# ======================================================
# COSINE SIMILARITY
# ======================================================

def cosine_similarity(embedding1, embedding2):

    return torch.nn.functional.cosine_similarity(
        embedding1.unsqueeze(0),
        embedding2.unsqueeze(0),
        dim=1,
    ).item()
