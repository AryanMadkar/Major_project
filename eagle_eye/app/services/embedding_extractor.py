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

        embedding = face.embedding
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