from pathlib import Path

import cv2

from app.services.frame_quality import (
    calculate_blur_score,
    calculate_brightness
)

FRAME_OUTPUT_DIR = Path(
    "extracted_frames"
)

BLUR_THRESHOLD = 100
BRIGHTNESS_THRESHOLD = 40

FRAME_INTERVAL = 5


def extract_frames(
    video_path,
    video_id
):

    cap = cv2.VideoCapture(
        str(video_path)
    )

    if not cap.isOpened():
        return {
            "success": False,
            "message": "Cannot open video"
        }

    session_dir = (
        FRAME_OUTPUT_DIR / video_id
    )

    session_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    frame_index = 0
    saved_frames = 0

    rejected_blur = 0
    rejected_dark = 0

    extracted_metadata = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        if frame_index % FRAME_INTERVAL != 0:
            frame_index += 1
            continue

        blur_score = calculate_blur_score(
            frame
        )

        brightness = calculate_brightness(
            frame
        )

        if blur_score < BLUR_THRESHOLD:
            rejected_blur += 1
            frame_index += 1
            continue

        if brightness < BRIGHTNESS_THRESHOLD:
            rejected_dark += 1
            frame_index += 1
            continue

        frame_filename = (
            f"frame_{saved_frames:04d}.jpg"
        )

        frame_path = (
            session_dir / frame_filename
        )

        cv2.imwrite(
            str(frame_path),
            frame
        )

        extracted_metadata.append({
            "frame_name": frame_filename,
            "blur_score": round(
                blur_score,
                2
            ),
            "brightness": round(
                brightness,
                2
            )
        })

        saved_frames += 1
        frame_index += 1

    cap.release()

    return {
        "success": True,
        "saved_frames": saved_frames,
        "rejected_blur": rejected_blur,
        "rejected_dark": rejected_dark,
        "frames_directory": str(
            session_dir
        ),
        "frames": extracted_metadata
    }