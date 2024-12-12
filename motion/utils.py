from math import cos, sin
import numpy as np


def BodyTransformationMatrix(roll, pitch, yaw, x, y, z):
    """
    Note: roll, pitch, yaw should be provided in radians.

    Parameters:
        - roll
        - pitch
        - yaw
        - x: x coordinate of the centre of the body
        - y: y coordinate of the centre of the body
        - z: z coordinate of the centre of the body

    Inspired by: https://www.researchgate.net/publication/322594373_Inverse_Kinematic_Analysis_of_a_Quadruped_Robot
    """
    Rx = np.array(
        [
            [1, 0, 0, 0],
            [0, cos(roll), -sin(roll), 0],
            [0, sin(roll), cos(roll), 0],
            [0, 0, 0, 1],
        ]
    )
    Ry = np.array(
        [
            [cos(pitch), 0, sin(pitch), 0],
            [0, 1, 0, 0],
            [-sin(pitch), 0, cos(pitch), 0],
            [0, 0, 0, 1],
        ]
    )
    Rz = np.array(
        [
            [cos(yaw), -sin(yaw), 0, 0],
            [sin(yaw), cos(yaw), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # All axes rotation matrix: roll -> pitch -> yaw.
    Rxyz = Rx @ Ry @ Rz

    # Translation matrix.
    T = np.array([[0, 0, 0, x], [0, 0, 0, y], [0, 0, 0, z], [0, 0, 0, 0]])

    # Transformation matrix.
    Tm = T + Rxyz

    return Tm


def JointAnglesProvider(leg, Tlf, Trf, Tlb, Trb, LegPoints):
    """
    Returns the joint angles from all four legs in the order:
        LF, LB, RF, RB
    """
    Ix = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    Qlf = np.linalg.inv(Tlf) @ LegPoints[0]
    plf = leg.ik(Qlf[0], Qlf[1], Qlf[2])

    Qlb = np.linalg.inv(Tlb) @ LegPoints[2]
    plb = leg.ik(Qlb[0], Qlb[1], Qlb[2])

    Qrf = Ix @ np.linalg.inv(Trf) @ LegPoints[1]
    prf = leg.ik(Qrf[0], Qrf[1], Qrf[2])

    Qrb = Ix @ np.linalg.inv(Trb) @ LegPoints[3]
    prb = leg.ik(Qrb[0], Qrb[1], Qrb[2])

    return (plf, plb, prf, prb)