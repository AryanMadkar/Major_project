from pathlib import Path

import cv2

MIN_FPS = 15
MIN_WIDTH = 640
MIN_HEIGHT = 480
MIN_DURATION = 2
MAX_DURATION = 20


def extract_video_metadata(
    video_path: str
):
    video_path = str(video_path)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "success": False,
            "message": "Cannot open video"
        }

    fps = cap.get(
        cv2.CAP_PROP_FPS
    )

    frame_count = int(
        cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    width = int(
        cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    height = int(
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    duration = 0

    if fps > 0:
        duration = round(
            frame_count / fps,
            2
        )

    cap.release()
    
    validation_errors = []

    if fps < MIN_FPS:
        validation_errors.append(
            "FPS too low"
        )

    if width < MIN_WIDTH:
        validation_errors.append(
            "Resolution too low"
        )

    if height < MIN_HEIGHT:
        validation_errors.append(
            "Resolution too low"
        )

    if duration < MIN_DURATION:
        validation_errors.append(
            "Video too short"
        )

    if duration > MAX_DURATION:
        validation_errors.append(
            "Video too long"
        )

    return {
        "success": True,
        "fps": round(fps, 2),
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "resolution": f"{width}x{height}",
        "duration_seconds": duration,
        "is_valid": len(validation_errors) == 0,
        "validation_errors": validation_errors
    }