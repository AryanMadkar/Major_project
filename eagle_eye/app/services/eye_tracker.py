from app.services.blink_detector import (
    LEFT_EYE,
    RIGHT_EYE
)


def extract_eye_points(
    landmarks,
    width,
    height
):

    left_eye_points = []
    right_eye_points = []

    for idx in LEFT_EYE:
        point = landmarks[idx]
        left_eye_points.append([
            point.x * width,
            point.y * height
        ])

    for idx in RIGHT_EYE:
        point = landmarks[idx]
        right_eye_points.append([
            point.x * width,
            point.y * height
        ])

    return left_eye_points, right_eye_points