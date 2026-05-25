from pathlib import Path
from urllib.request import urlretrieve

import cv2
import mediapipe as mp

from app.services.blink_detector import (
    calculate_ear
)
from app.services.eye_tracker import (
    extract_eye_points
)


BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
MODEL_PATH = Path(
    __file__
).resolve().parent / "models" / "face_landmarker.task"


def ensure_model_file():
    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if MODEL_PATH.exists():
        return MODEL_PATH

    urlretrieve(
        MODEL_URL,
        MODEL_PATH
    )

    return MODEL_PATH

landmarker_options = FaceLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(
            ensure_model_file()
        )
    ),
    running_mode=RunningMode.IMAGE,
    num_faces=1,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

face_landmarker = FaceLandmarker.create_from_options(
    landmarker_options
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

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        results = face_landmarker.detect(
            mp_image
        )

        if not results.face_landmarks:
            no_face_frames += 1
            continue

        landmarks = (
            results
            .face_landmarks[0]
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