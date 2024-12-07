from math import cos, sin
import numpy as np


def BodyTransformationMatrix(roll, pitch, yaw, xb, yb, zb):
    """
    Note: roll, pitch, yaw should be provided in radians.

    Parameters:
        - roll
        - pitch
        - yaw
        - xb: x coordinate of the centre of the body
        - yb: y coordinate of the centre of the body
        - zb: z coordinate of the centre of the body
    
    Heavily inspired by: https://www.researchgate.net/publication/322594373_Inverse_Kinematic_Analysis_of_a_Quadruped_Robot
    """
    X = np.matrix(
        [
            [1, 0, 0, 0],
            [0, cos(roll), -sin(roll), 0],
            [0, sin(roll), cos(roll), 0],
            [0, 0, 0, 1],
        ]
    )
    Y = np.matrix(
        [
            [cos(pitch), 0, sin(pitch), 0],
            [0, 1, 0, 0],
            [-sin(pitch), 0, cos(pitch), 0],
            [0, 0, 0, 1],
        ]
    )
    Z = np.matrix(
        [
            [cos(yaw), -sin(yaw), 0, 0],
            [sin(yaw), cos(yaw), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # Rotation matrix: roll -> pitch -> yaw.
    RotMat = X @ Y @ Z

    # Translation matrix for the body centre.
    BodyCentre = np.matrix([[1, 0, 0, xb], [0, 1, 0, yb], [0, 0, 1, zb], [0, 0, 0, 1]])

    T = RotMat @ BodyCentre

    return T
