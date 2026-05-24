import numpy as np


LEFT_EYE = [
    33,
    160,
    158,
    133,
    153,
    144
]

RIGHT_EYE = [
    362,
    385,
    387,
    263,
    373,
    380
]


def euclidean_distance(
    p1,
    p2
):

    return np.linalg.norm(
        np.array(p1) - np.array(p2)
    )


def calculate_ear(
    eye_points
):

    vertical_1 = euclidean_distance(
        eye_points[1],
        eye_points[5]
    )

    vertical_2 = euclidean_distance(
        eye_points[2],
        eye_points[4]
    )

    horizontal = euclidean_distance(
        eye_points[0],
        eye_points[3]
    )

    ear = (
        vertical_1 + vertical_2
    ) / (2.0 * horizontal)

    return ear