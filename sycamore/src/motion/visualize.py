import numpy as np
import rerun as rr
from ik import BodyIK, LegIK
from math import radians, pi, sin, cos
import time


def draw_robot(leg, body, T, LegPoints):
    """
    Inspired by:
        - https://spotmicroai.readthedocs.io/en/latest/kinematic/#setup-our-3d-ouput
    """
    (Tlf, Trf, Tlb, Trb, Tm) = T

    robot_body = body.log_body(body.calc_segments(Tlf, Trf, Tlb, Trb, Tm))

    # Invert local X
    Ix = np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    Q = np.linalg.inv(Tlf) @ LegPoints[0]
    p = [Tlf @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    left_front = leg.log_legs(p)

    Q = np.linalg.inv(Tlb) @ LegPoints[2]
    p = [Tlb @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    left_back = leg.log_legs(p)

    Q = Ix @ np.linalg.inv(Trf) @ LegPoints[1]
    p = [Trf @ Ix @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
    right_front = leg.log_legs(p)

    Q = Ix @ np.linalg.inv(Trb) @ LegPoints[3]
    p = [Trb @ Ix @ x for x in leg.calc_segments(leg.ik(Q[0], Q[1], Q[2]))]
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


def little_dance(leg, body):
    LegPoints = np.array(
        [
            [100, -100, 100, 1],
            [100, -100, -100, 1],
            [-100, -100, 100, 1],
            [-100, -100, -100, 1],
        ]
    )

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


def twerk(leg, body):
    LegPoints = np.array(
        [
            [100, -60, 100, 1],
            [100, -60, -100, 1],
            [-100, -100, 100, 1],
            [-100, -100, -100, 1],
        ]
    )
    t = [-100, -90, -80, -70, -60, -50, -60, -70, -80, -90]
    t_array = []
    t_array.extend(t * 50)
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)

    for point in t_array:
        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)
        LegPoints[2][1] = point
        LegPoints[3][1] = point
        time.sleep(0.1)


def majestic_gallop(leg, body):
    LegPoints = np.array(
        [
            [100, -100, 100, 1],
            [100, -100, -100, 1],
            [-100, -100, 100, 1],
            [-100, -100, -100, 1],
        ]
    )
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
    radius = 20
    points = point_on_a_circle(radius, 100)
    for point in points:
        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)
        LegPoints = np.array(
            [
                [point[0] + 100, point[1] + -100, 100, 1],
                [point[0] + 100, point[1] + -100, -100, 1],
                [point[0] + -100, point[1] + -100, 100, 1],
                [point[0] + -100, point[1] + -100, -100, 1],
            ]
        )
        time.sleep(0.01)


def point_on_a_circle(radius, nr_of_revolutions):
    points = []
    for theta in np.linspace(0, nr_of_revolutions * pi, 100 * nr_of_revolutions):
        x = radius * sin(theta)
        y = radius * cos(theta)
        points.append([x, y])
    return points


def reset_body(leg, body):
    LegPoints = np.array(
        [
            [100, -100, 100, 1],
            [100, -100, -100, 1],
            [-100, -100, 100, 1],
            [-100, -100, -100, 1],
        ]
    )
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
    draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)


def init_rerun():
    rr.init("IK visualization")
    rr.connect_tcp("127.0.0.1:9876")


if __name__ == "__main__":
    init_rerun()
    l1 = 25
    l2 = 20
    l3 = 80
    l4 = 80
    length = 150
    width = 90
    leg = LegIK(l1, l2, l3, l4)
    body = BodyIK(length, width)
    reset_body(leg, body)
    little_dance(leg, body)
    # majestic_gallop(leg, body)
    # twerk(leg, body)
