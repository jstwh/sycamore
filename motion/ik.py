"""
Inverse kinematics of Quad-EX.

Inspired by:
    - https://www.researchgate.net/publication/322594373_Inverse_Kinematic_Analysis_of_a_Quadruped_Robot
    - https://github.com/adham-elarabawy/open-quadruped/tree/master
    - https://spotmicroai.readthedocs.io
    - https://github.com/engineerm-jp/Inverse_Kinematics_YouTube/tree/main
"""

from math import cos, sin, atan2, sqrt, acos, pi
import numpy as np
from motion.utils import BodyTransformationMatrix


class LegIK:
    """
    Inverse kinematics for a 3 DoF quadruped leg. Returns the joint angles for the provided
    desired end position [x, y, z].

    l1: length of offset1 in the shoulder.
    l2: length of offset2 in the shoulder.
    l3: length of the upper leg segment.
    l4: length of the lower leg segment.
    """

    def __init__(self, l1, l2, l3, l4):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.l4 = l4

    def ik(self, x, y, z) -> tuple[float, float, float]:
        l1 = self.l1
        l2 = self.l2
        l3 = self.l3
        l4 = self.l4

        try:
            F = sqrt(x**2 + y**2 - l1**2)
            G = F - l2
            H = sqrt(G**2 + z**2)
            theta1 = -atan2(y, x) - atan2(F, -l1)
            D = (H**2 - l3**2 - l4**2) / (2 * l3 * l4)
            theta3 = acos(D)
            theta2 = atan2(z, G) - atan2(l4 * sin(theta3), l3 + l4 * cos(theta3))
        except ValueError:
            return None, None, None

        return theta1, theta2, theta3

    def calc_segments(self, angles):
        """
        Calculates the leg segments based on the angles from the inverse kinematics. This is
        used to visualize the segments in rerun.
        """
        (theta1, theta2, theta3) = angles
        theta23 = theta2 + theta3
        l1 = self.l1
        l2 = self.l2
        l3 = self.l3
        l4 = self.l4

        T0 = np.array([0, 0, 0, 1])
        T1 = T0 + np.array([-l1 * cos(theta1), l1 * sin(theta1), 0, 0])
        T2 = T1 + np.array([-l2 * sin(theta1), -l2 * cos(theta1), 0, 0])
        T3 = T2 + np.array(
            [
                -l3 * sin(theta1) * cos(theta2),
                -l3 * cos(theta1) * cos(theta2),
                l3 * sin(theta2),
                0,
            ]
        )
        T4 = T3 + np.array(
            [
                -l4 * sin(theta1) * cos(theta23),
                -l4 * cos(theta1) * cos(theta23),
                l4 * sin(theta23),
                0,
            ]
        )

        return np.array([T0, T1, T2, T3, T4])

    def log_legs(self, p):
        """
        Log the leg data from [calc_segments] to rerun.
        Returns something that can be directly passed into a rr.LineStrips3D.
        """
        p1 = np.array([p[0][0], p[0][2], p[0][1]])
        p2 = np.array([p[1][0], p[1][2], p[1][1]])
        p3 = np.array([p[2][0], p[2][2], p[2][1]])
        p4 = np.array([p[3][0], p[3][2], p[3][1]])
        p5 = np.array([p[4][0], p[4][2], p[4][1]])

        return np.array([p1, p2, p3, p4, p5])


class BodyIK:
    """
    Inverse kinematics for a 12 DoF quadruped body.

    Allows for direct manipulation of the body around it's six axes.

    Variables:
        - Tm: Transformation Matrix.
        - Trb,Trf,Tlb,Tlf: Transformation matrix for RightBack, RightFront, LeftBack and LeftFront.
    """

    def __init__(self, length, width):
        self.length = length
        self.width = width

    def ik(self, yaw, pitch, roll, x, y, z):
        """
        Note: roll, pitch, yaw should be provided in radians.
        """
        Tm = BodyTransformationMatrix(roll, pitch, yaw, x, y, z)

        Trb = Tm @ np.array(
            [
                [cos(pi / 2), 0, sin(pi / 2), -self.length / 2],
                [0, 1, 0, 0],
                [-sin(pi / 2), 0, cos(pi / 2), -self.width / 2],
                [0, 0, 0, 1],
            ]
        )

        Trf = Tm @ np.array(
            [
                [cos(pi / 2), 0, sin(pi / 2), self.length / 2],
                [0, 1, 0, 0],
                [-sin(pi / 2), 0, cos(pi / 2), -self.width / 2],
                [0, 0, 0, 1],
            ]
        )

        Tlf = Tm @ np.array(
            [
                [cos(pi / 2), 0, sin(pi / 2), self.length / 2],
                [0, 1, 0, 0],
                [-sin(pi / 2), 0, cos(pi / 2), self.width / 2],
                [0, 0, 0, 1],
            ]
        )

        Tlb = Tm @ np.array(
            [
                [cos(pi / 2), 0, sin(pi / 2), -self.length / 2],
                [0, 1, 0, 0],
                [-sin(pi / 2), 0, cos(pi / 2), self.width / 2],
                [0, 0, 0, 1],
            ]
        )

        return (Tlf, Trf, Tlb, Trb, Tm)

    def calc_segments(self, Tlf, Trf, Tlb, Trb, Tm):
        """
        FP stands for Foot Point. It represents the coordinates of a foot in the local reference frame,
        expressed as a 4D vector ([x, y, z, 1]). The extra 1 is for homogeneous coordinates,
        enabling matrix transformations.

        CP stands for Contact Point. It is the transformed position of the foot in the world (or body)
        frame, calculated by applying the transformation matrices (Tlf, Trf, Tlb, Trb) to the FP.

        These concepts are used to determine the positions of the robot's feet after applying body
        transformations, which include rotation and translation. The transformation matrices encode
        the effect of body pose changes on the foot positions.
        """
        FP = [0, 0, 0, 1]
        CP = [x @ FP for x in [Tlf, Trf, Tlb, Trb]]
        return CP

    def log_body(self, CP):
        """
        Log the body data from [calc_segments] to rerun.
        Returns something that can be directly passed into a rr.LineStrips3D.
        """
        p1 = np.array([CP[0][0], CP[0][2], CP[0][1]])
        p2 = np.array([CP[1][0], CP[1][2], CP[1][1]])
        p3 = np.array([CP[3][0], CP[3][2], CP[3][1]])
        p4 = np.array([CP[2][0], CP[2][2], CP[2][1]])
        p5 = np.array([CP[0][0], CP[0][2], CP[0][1]])

        return np.array([p1, p2, p3, p4, p5])
