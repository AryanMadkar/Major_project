from pathlib import Path

import cv2
import mediapipe as mp

from app.services.blink_detector import (
    calculate_ear
)
from app.services.eye_tracker import (
    extract_eye_points
)


mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

BLINK_THRESHOLD = 0.20


def analyze_liveness(
    frames_directory
):

    frames_directory = Path(
        frames_directory
    )

    blink_frames = 0
    total_frames = 0
    no_face_frames = 0

    ear_values = []

    for frame_path in frames_directory.glob(
        "*.jpg"
    ):

        image = cv2.imread(
            str(frame_path)
        )

        if image is None:
            continue

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        results = face_mesh.process(
            rgb
        )

        if not results.multi_face_landmarks:
            no_face_frames += 1
            continue

        landmarks = (
            results
            .multi_face_landmarks[0]
            .landmark
        )

        height, width, _ = image.shape

        left_eye_points, right_eye_points = extract_eye_points(
            landmarks,
            width,
            height
        )

        left_ear = calculate_ear(
            left_eye_points
        )

        right_ear = calculate_ear(
            right_eye_points
        )

        avg_ear = (
            left_ear + right_ear
        ) / 2.0

        ear_values.append(avg_ear)

        if avg_ear < BLINK_THRESHOLD:
            blink_frames += 1

        total_frames += 1

    blink_ratio = blink_frames / max(total_frames, 1)

    live_confidence = min(
        1.0,
        (blink_ratio * 0.7) + min(total_frames, 10) / 20.0
    )

    is_live = blink_frames > 0 and total_frames > 0

    return {
        "success": True,
        "total_frames":
            total_frames,
        "no_face_frames":
            no_face_frames,
        "blink_frames":
            blink_frames,
        "is_live":
            is_live,
        "live_confidence":
            round(
                live_confidence,
                4
            ),
        "avg_ear":
            round(
                sum(ear_values)
                / max(len(ear_values), 1),
                4
            )
    }