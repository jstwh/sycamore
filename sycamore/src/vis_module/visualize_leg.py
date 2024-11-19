import numpy as np
import matplotlib.pyplot as plt
import math


class Leg:
    def __init__(self, l1: int, l2: int):
        # l1, l2 lengths of the upper and lower leg respectively
        self.l1 = l1
        self.l2 = l2

    def ja_from_xy(self, x: float, y: float) -> tuple[int, int]:
        D = (x**2 + y**2 - self.l1**2 - self.l2**2) / (2 * self.l1 * self.l2)

        try:
            theta2 = math.acos(D)  # theta2 in radians
        except ValueError:
            print("Out of bounds")
            return None

        # Calculate theta1
        theta1 = math.atan2(y, x) - math.atan2(
            self.l2 * math.sin(theta2), self.l1 + self.l2 * math.cos(theta2)
        )

        return (math.degrees(theta1), math.degrees(theta2))

    def xy_from_ja(self, theta1: float, theta2: float) -> tuple[int, int]:
        # Convert degrees to radians for trigonometric functions
        theta1_rad = math.radians(theta1)
        theta2_rad = math.radians(theta2)

        x1 = self.l1 * math.cos(theta1_rad)
        y1 = self.l1 * math.sin(theta1_rad)

        x2 = x1 + self.l2 * math.cos(theta1_rad + theta2_rad)
        y2 = y1 + self.l2 * math.sin(theta1_rad + theta2_rad)

        print(f"Joint 1 (x1, y1): ({int(x1)}, {int(y1)})")
        print(f"Joint 2 (x2, y2): ({int(x2)}, {int(y2)})")
        return (int(x2), int(y2))


def draw_leg(x, y, l1, l2):
    leg = Leg(l1, l2)
    theta1, theta2 = leg.ja_from_xy(x, y)
    print(f"theta1: {theta1}, theta2: {theta2}")

    theta1 = np.radians(theta1)
    theta2 = np.radians(theta2)

    x0, y0 = 0, 0

    # forward kinematics, super easy cus planar
    x1 = l1 * np.cos(theta1)
    y1 = l1 * np.sin(theta1)

    x2 = x1 + l2 * np.cos(theta1 + theta2)
    y2 = y1 + l2 * np.sin(theta1 + theta2)

    # for my sanity
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)

    print(f"Joint 1 (x1, y1): ({x1}, {y1})")
    print(f"Joint 2 (x2, y2): ({x2}, {y2})")

    plt.figure()
    plt.plot([x0, x1], [y0, y1])
    plt.plot([x1, x2], [y1, y2])

    plt.xlim(-l1 - l2, l1 + l2)
    plt.ylim(-l1 - l2, l1 + l2)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.gca().set_aspect("equal")

    plt.show()


if __name__ == "__main__":
    l1 = 100
    l2 = 100

    x = 0
    y = 138
    draw_leg(x, y, l1, l2)
