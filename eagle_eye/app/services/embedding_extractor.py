from pathlib import Path

import cv2
import numpy as np
import torch

from sklearn.preprocessing import normalize


class SimpleEmbeddingModel:

    def __init__(self):

        self.embedding_size = 512

    def generate_embedding(
        self,
        image
    ):

        resized = cv2.resize(
            image,
            (112, 112)
        )

        embedding = np.random.rand(
            self.embedding_size
        )

        embedding = normalize(
            embedding.reshape(1, -1)
        )[0]

        return embedding


model = SimpleEmbeddingModel()


def extract_embeddings(
    aligned_faces_dir
):

    aligned_faces_dir = Path(
        aligned_faces_dir
    )

    embeddings = []

    for face_path in aligned_faces_dir.glob(
        "*.jpg"
    ):

        image = cv2.imread(
            str(face_path)
        )

        embedding = (
            model.generate_embedding(
                image
            )
        )

        embeddings.append({
            "face_file":
                face_path.name,
            "embedding":
                embedding.tolist()
        })

    return {
        "success": True,
        "total_embeddings":
            len(embeddings),
        "embeddings":
            embeddings
    }