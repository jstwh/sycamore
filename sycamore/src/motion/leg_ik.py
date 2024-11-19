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


if __name__ == "__main__":
    l1 = 100
    l2 = 100
    leg = Leg(l1, l2)

    x = 1
    y = 140

    while True:
        user_input = input("Press w, a, s, d \n")
        if user_input not in ["w", "a", "s", "d"]:
            print("Invalid")
            continue

        if user_input == "w":
            y += 5
        elif user_input == "a":
            x -= 5
        elif user_input == "s":
            y -= 5
        elif user_input == "d":
            x += 5

        if (result := leg.ja_from_xy(x, y)) is not None:
            t1, t2 = result
            leg.xy_from_ja(t1, t2)
        else:
            print("Calculation failed due to out of bounds")
