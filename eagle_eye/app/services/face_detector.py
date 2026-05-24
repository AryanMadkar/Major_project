from pathlib import Path

import cv2

from insightface.app import FaceAnalysis


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

    save_dir.mkdir(
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

        faces = app.get(image)

        if len(faces) == 0:
            rejected_no_face += 1
            continue

        if len(faces) > 1:
            rejected_multiple_faces += 1
            continue

        face = faces[0]

        bbox = face.bbox.astype(int)

        x1, y1, x2, y2 = bbox

        cropped_face = image[
            y1:y2,
            x1:x2
        ]

        face_filename = (
            f"{frame_path.stem}_face.jpg"
        )

        face_path = (
            save_dir / face_filename
        )

        cv2.imwrite(
            str(face_path),
            cropped_face
        )

        detected_faces.append({
            "frame": frame_path.name,
            "face_file": face_filename,
            "bbox": bbox.tolist(),
            "confidence": float(
                face.det_score
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
        "faces": detected_faces
    }