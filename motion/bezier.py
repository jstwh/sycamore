import math
import numpy as np
from leg_ik import Leg
import rerun as rr
import time


def main():
    rr.init("IK visualization")
    rr.connect_tcp("127.0.0.1:9876")

    radius = 20
    points = point_on_a_circle(radius, 20)
    l1 = 100
    l2 = 100
    leg = Leg(l1, l2)
    update_pos(points, leg)


def update_pos(points, leg):
    for idx, point in enumerate(points):
        t1, t2 = leg.ja_from_xy(point[0], point[1])
        upper, lower = leg.xy_from_ja(t1, t2)

        rr.log(
            "leg_data",
            rr.LineStrips3D(
                [upper, lower],
                colors=[[255, 0, 0], [0, 255, 0]],
                labels=["upper leg", "lower leg"],
                radii=1.5,
            ),
        )

        if idx == 1:
            time.sleep(3)
        else:
            time.sleep(0.01)


def point_on_a_circle(radius, nr_of_revolutions):
    points = []
    # five circles
    for theta in np.linspace(0, nr_of_revolutions * math.pi, 100 * nr_of_revolutions):
        x = radius * math.sin(theta)
        y = radius * math.cos(theta) - 130
        points.append([x, y])
    return points


if __name__ == "__main__":
    main()
