from pathlib import Path

import cv2
import numpy as np


ALIGNED_OUTPUT_DIR = Path(
    "aligned_faces"
)

DESIRED_SIZE = (224, 224)


def align_face(
    image,
    landmarks
):

    left_eye = landmarks[0]
    right_eye = landmarks[1]

    left_eye_x, left_eye_y = left_eye
    right_eye_x, right_eye_y = right_eye

    delta_x = (
        right_eye_x - left_eye_x
    )

    delta_y = (
        right_eye_y - left_eye_y
    )

    angle = np.degrees(
        np.arctan2(
            delta_y,
            delta_x
        )
    )

    eyes_center = (
        (
            left_eye_x + right_eye_x
        ) // 2,
        (
            left_eye_y + right_eye_y
        ) // 2
    )

    rotation_matrix = (
        cv2.getRotationMatrix2D(
            eyes_center,
            angle,
            1.0
        )
    )

    aligned_image = cv2.warpAffine(
        image,
        rotation_matrix,
        (
            image.shape[1],
            image.shape[0]
        ),
        flags=cv2.INTER_CUBIC
    )

    aligned_image = cv2.resize(
        aligned_image,
        DESIRED_SIZE
    )

    return aligned_image, angle