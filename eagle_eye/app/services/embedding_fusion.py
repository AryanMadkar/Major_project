import numpy as np

from sklearn.preprocessing import (
    normalize
)


def fuse_embeddings(
    embeddings
):

    embeddings = np.array(
        embeddings
    )

    mean_embedding = np.mean(
        embeddings,
        axis=0
    )

    normalized_embedding = normalize(
        mean_embedding.reshape(1, -1)
    )[0]

    return normalized_embedding