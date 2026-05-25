from pathlib import Path

import cv2
import numpy as np
from insightface.app import FaceAnalysis


app = FaceAnalysis(
    providers=["CPUExecutionProvider"]
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


def extract_embeddings(
    aligned_faces_dir
):

    def get_face_embedding(face):
        normed_embedding = getattr(
            face,
            "normed_embedding",
            None
        )

        if normed_embedding is not None:
            return np.asarray(
                normed_embedding,
                dtype=np.float32
            ).reshape(-1)

        embedding = getattr(
            face,
            "embedding",
            None
        )

        if embedding is None:
            return None

        embedding = np.asarray(
            embedding,
            dtype=np.float32
        ).reshape(-1)

        norm = np.linalg.norm(
            embedding
        )

        if norm == 0:
            return None

        return embedding / norm

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

        if image is None:
            continue

        faces = app.get(image)

        if len(faces) == 0:
            continue

        face = faces[0]

        embedding = get_face_embedding(
            face
        )

        if embedding is None:
            continue

        embedding_norm = np.linalg.norm(
            embedding
        )

        embeddings.append({
            "face_file":
                face_path.name,
            "embedding":
                embedding.tolist(),
            "embedding_norm": float(
                embedding_norm
            )
        })

    return {
        "success": True,
        "total_embeddings":
            len(embeddings),
        "embeddings":
            embeddings
    }