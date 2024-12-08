import numpy as np
import rerun as rr
from ik import BodyIK, LegIK
from math import radians


def draw_robot():
    l1 = 25
    l2 = 20
    l3 = 80
    l4 = 80
    length = 150
    width = 90
    leg = LegIK(l1, l2, l3, l4)
    body = BodyIK(length, width)
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(
        radians(0), radians(0), radians(0), 0, 0, 0
    )

    # These points define the initial positions of the robot's body in its local reference frame.
    Lp = np.array(
        [
            [100, -100, 100, 1],
            [100, -100, -100, 1],
            [-100, -100, 100, 1],
            [-100, -100, -100, 1],
        ]
    )

    body = body.log_body(body.calc_segments(Tlf, Trf, Tlb, Trb, Tm))

    # Invert local X
    Ix = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    Q = np.linalg.inv(Tlf) @ Lp[0]
    p = [Tlf @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    left_front = leg.log_legs(p)

    Q = np.linalg.inv(Tlb) @ Lp[2]
    p = [Tlb @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    left_back = leg.log_legs(p)

    Q = Ix @ np.linalg.inv(Trf) @ Lp[1]
    p = [Trf @ Ix @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    right_front = leg.log_legs(p)

    Q = Ix @ np.linalg.inv(Trb) @ Lp[3]
    p = [Trb @ Ix @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    right_back = leg.log_legs(p)

    rr.log(
        "robot",
        rr.LineStrips3D(
            [
                body,
                right_front,
                right_back,
                left_front,
                left_back,
            ],
        ),
    )


def init_rerun():
    rr.init("IK visualization")
    rr.connect_tcp("127.0.0.1:9876")


if __name__ == "__main__":
    init_rerun()
    draw_robot()
