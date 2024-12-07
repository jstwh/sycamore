import math
import numpy as np
from utils import BodyTransformationMatrix


class LegIK:
    """
    Inverse kinematics for a 3 DoF quadruped leg. Returns the joint angles for the provided 
    desired end position [x, y, z].

    l1: length of the offset in the shoulder.
    l2: length of the upper leg segment.
    l3: length of the lower leg segment.

    Note: Sizes are presumed in meters.
    """
    def __init__(self, l1, l2, l3):
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def ik(self, coordinates, leg_position) -> tuple[float, float, float]:
        x, y, z = coordinates
        l1 = self.l1
        l2 = self.l2
        l3 = self.l3

        try:
            d = (x**2 + y**2 + z**2 - l1**2 - l2**2 - l3**2) / (2 * l2 * l3)
            theta1 = -math.atan2(-y, x) - math.atan2(
                math.sqrt(x**2 + y**2 - l1**2), -(l1**2)
            )
            if leg_position == "right":
                theta3 = math.atan2(math.sqrt(1 - d**2), d)
            elif leg_position == "left":
                theta3 = math.atan2(-math.sqrt(1 - d**2), d)
            theta2 = math.atan2(z, math.sqrt(x**2 + y**2 - l1**2)) - math.atan2(
                l3 * math.sin(theta3), l2 + l3 * math.cos(theta3)
            )
        except ValueError:
            return None, None, None

        return (theta1, theta2, theta3)


class BodyIK:
    """
    Inverse kinematics for a 12 DoF quadruped body.

    Allows for direct manipulation of the body around it's six axes.

    Note: Sizes are presumed in meters.
    """
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height

    def ik(self, yaw, pitch, roll, x, y, z):
        pass


if __name__ == "__main__":
    # All lengths are in meters
    l1 = 0.1
    l2 = 0.4
    l3 = 0.4
    x = 0.0
    y = -0.6
    z = 0.0
    coords = (x, y, z)
    position = "left"

    leg = LegIK(l1, l2, l3)

    t1, t2, t3 = leg.ik(coords, position)
    print(math.degrees(t1), math.degrees(t2), math.degrees(t3))
