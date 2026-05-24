from pathlib import Path

import cv2

from insightface.app import FaceAnalysis
from app.services.face_aligner import (
    align_face
)

FACE_OUTPUT_DIR = Path(
    "detected_faces"
)

app = FaceAnalysis(
    providers=["CPUExecutionProvider"]
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


def detect_faces(
    frames_directory,
    video_id
):

    frames_directory = Path(
        frames_directory
    )

    save_dir = (
        FACE_OUTPUT_DIR / video_id
    )

    aligned_dir = Path(
        "aligned_faces"
    ) / video_id

    save_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    aligned_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    detected_faces = []

    rejected_multiple_faces = 0
    rejected_no_face = 0

    for frame_path in frames_directory.glob(
        "*.jpg"
    ):

        image = cv2.imread(
            str(frame_path)
        )

        if image is None:
            continue

        faces = app.get(image)

        if len(faces) == 0:
            rejected_no_face += 1
            continue

        if len(faces) > 1:
            rejected_multiple_faces += 1
            continue

        face = faces[0]

        landmarks = face.kps.astype(int)

        bbox = face.bbox.astype(int)

        x1, y1, x2, y2 = bbox

        height, width = image.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        if x2 <= x1 or y2 <= y1:
            continue

        cropped_face = image[
            y1:y2,
            x1:x2
        ]

        normalized_landmarks = []

        for point in landmarks:
            px, py = point

            normalized_landmarks.append([
                px - x1,
                py - y1
            ])

        aligned_face, rotation_angle = align_face(
            cropped_face,
            normalized_landmarks
        )

        face_filename = (
            f"{frame_path.stem}_face.jpg"
        )

        face_path = (
            save_dir / face_filename
        )

        aligned_filename = (
            f"{frame_path.stem}_aligned.jpg"
        )

        aligned_path = (
            aligned_dir / aligned_filename
        )

        cv2.imwrite(
            str(face_path),
            cropped_face
        )

        cv2.imwrite(
            str(aligned_path),
            aligned_face
        )

        detected_faces.append({
            "frame": frame_path.name,
            "face_file": face_filename,
            "aligned_file": aligned_filename,
            "bbox": bbox.tolist(),
            "confidence": float(
                face.det_score
            ),
            "rotation_angle": round(
                float(rotation_angle),
                2
            )
        })

    return {
        "success": True,
        "detected_faces": len(
            detected_faces
        ),
        "rejected_no_face": rejected_no_face,
        "rejected_multiple_faces":
            rejected_multiple_faces,
        "faces_directory": str(
            save_dir
        ),
        "aligned_directory": str(
            aligned_dir
        ),
        "faces": detected_faces
    }