import math


class Leg:
    def __init__(self, l1: int, l2: int):
        # l1, l2 lengths of the upper and lower leg respectively
        self.l1 = l1
        self.l2 = l2

    def ja_from_xy(self, x: float, y: float) -> tuple[int, int]:
        """
        Inverse Kinematics
        """
        D = (x**2 + y**2 - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)

        try:
            theta2 = math.acos(D)
        except ValueError:
            print("Out of bounds")

        theta1 = math.atan2(y, x) - math.atan2(
            self.l2 * math.sin(theta2), self.l1 + self.l2 * math.cos(theta2)
        )

        return (math.degrees(theta1), math.degrees(theta2))

    def xy_from_ja(self, theta1: float, theta2: float):
        """
        Forward Kinematics (not rlly the correct return type but sketchy fix for now)
        """
        theta1 = math.radians(theta1)
        theta2 = math.radians(theta2)

        x0 = 0
        y0 = 0

        x1 = self.l1 * math.cos(theta1)
        y1 = self.l1 * math.sin(theta1)

        x2 = x1 + self.l2 * math.cos(theta1 + theta2)
        y2 = y1 + self.l2 * math.sin(theta1 + theta2)

        print(f"Joint 1 (x1, y1): ({int(x1)}, {int(y1)})")
        print(f"Joint 2 (x2, y2): ({int(x2)}, {int(y2)})")

        # return leg coordinates
        return [[x0, y0, 0], [x1, y1, 0]], [[x1, y1, 0], [x2, y2, 0]]
