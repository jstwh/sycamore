import numpy as np
import rerun as rr
from motion.ik import BodyIK, LegIK
from math import radians, pi, sin, cos, degrees
from motion.utils import JointAnglesProvider
import time


def draw_robot(leg, body, T, LegPoints):
    """
    Inspired by:
        - https://spotmicroai.readthedocs.io
    """
    (Tlf, Trf, Tlb, Trb, Tm) = T
    Ix = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    robot_body = body.log_body(body.calc_segments(Tlf, Trf, Tlb, Trb, Tm))
    Lf, Lb, Rf, Rb = JointAnglesProvider(leg, Tlf, Trf, Tlb, Trb, LegPoints)

    p = [Tlf @ x for x in leg.calc_segments(Lf)]
    left_front = leg.log_legs(p)

    p = [Tlb @ x for x in leg.calc_segments(Lb)]
    left_back = leg.log_legs(p)

    p = [Trf @ Ix @ x for x in leg.calc_segments(Rf)]
    right_front = leg.log_legs(p)

    p = [Trb @ Ix @ x for x in leg.calc_segments(Rb)]
    right_back = leg.log_legs(p)

    rr.log(
        "robot",
        rr.LineStrips3D(
            [
                robot_body,
                right_front,
                right_back,
                left_front,
                left_back,
            ],
        ),
    )


def little_dance(leg, body, LegPoints):
    angles_pitch = []
    angles_yaw = []
    angles_roll = []
    angles = [
        0,
        -5,
        -10,
        -15,
        -20,
        -25,
        -30,
        -25,
        -20,
        -15,
        -10,
        -5,
        0,
        5,
        10,
        15,
        20,
        25,
        30,
        25,
        20,
        15,
        10,
        5,
        0,
    ]

    angles_pitch.extend(angles * 2)
    angles_yaw.extend(angles * 2)
    angles_roll.extend(angles * 2)

    for angle in angles_pitch:
        time.sleep(0.1)
        (Tlf, Trf, Tlb, Trb, Tm) = body.ik(
            radians(angle), radians(0), radians(0), 0, 0, 0
        )

        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)

    for angle in angles_yaw:
        time.sleep(0.1)
        (Tlf, Trf, Tlb, Trb, Tm) = body.ik(
            radians(0), radians(angle), radians(0), 0, 0, 0
        )

        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)

    for angle in angles_roll:
        time.sleep(0.1)
        (Tlf, Trf, Tlb, Trb, Tm) = body.ik(
            radians(0), radians(0), radians(angle), 0, 0, 0
        )

        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)


def twerk(leg, body, LegPoints):
    t = [-100, -90, -80, -70, -60, -50, -60, -70, -80, -90]
    t_array = []
    t_array.extend(t * 50)
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)

    for point in t_array:
        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)
        LegPoints[2][1] = point
        LegPoints[3][1] = point
        time.sleep(0.1)


def majestic_gallop(leg, body, LegPoints):
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
    radius = 20
    points = point_on_a_circle(radius, 100)
    for point in points:
        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)
        LegPoints = np.array(
            [
                [point[0] + 210, point[1] + -200, 110, 1],
                [point[0] + 210, point[1] + -200, -110, 1],
                [point[0] + -210, point[1] + -200, 110, 1],
                [point[0] + -210, point[1] + -200, -110, 1],
            ]
        )
        LegPoints[:, 0] += point[0]
        LegPoints[:, 1] += point[1]
        time.sleep(0.01)


def point_on_a_circle(radius, nr_of_revolutions):
    points = []
    for theta in np.linspace(0, nr_of_revolutions * pi, 100 * nr_of_revolutions):
        x = radius * sin(theta)
        y = radius * cos(theta)
        points.append([x, y])
    return points


def reset_body(leg, body, LegPoints):
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
    draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)


def init_rerun():
    rr.init("IK visualization")
    rr.connect_tcp("127.0.0.1:9876")


if __name__ == "__main__":
    init_rerun()
    # LegPoints = np.array(
    #     [
    #         [210, -200, 110, 1],
    #         [210, -200, -110, 1],
    #         [-210, -200, 110, 1],
    #         [-210, -200, -110, 1],
    #     ]
    # ).astype(float)
    # LegPoints = np.array(
    #     [
    #         [100, -100, 100, 1],
    #         [100, -100, -100, 1],
    #         [-100, -100, 100, 1],
    #         [-100, -100, -100, 1],
    #     ]
    # ).astype(float)
    LegPoints = np.array(
        [
            [100, -100, 75, 1],
            [100, -100, -75, 1],
            [-100, -100, 75, 1],
            [-100, -100, -75, 1],
        ]
    ).astype(float)
    # l1 = 56
    # l2 = 1
    # l3 = 151
    # l4 = 176
    # length = 420
    # width = 220
    l1 = 20
    l2 = 0
    l3 = 80
    l4 = 80
    length = 160
    width = 110
    leg = LegIK(l1, l2, l3, l4)
    body = BodyIK(length, width)
    reset_body(leg, body, LegPoints)
    little_dance(leg, body, LegPoints)
    # majestic_gallop(leg, body, LegPoints)
    # twerk(leg, body, LegPoints)
