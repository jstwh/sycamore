from adafruit_servokit import ServoKit
import time
import numpy as np
from motion.ik import BodyIK, LegIK
from motion.step_planner import TrotGait
from motion.visualize import reset_body, draw_robot
from math import radians, degrees
import rerun as rr
from motion.utils import JointAnglesProvider


def main():
    rr.init("IK visualization")
    rr.connect_tcp("145.109.45.135:9876")
    kit = ServoKit(channels=16)
    kit.servo[0].set_pulse_width_range(500, 2500)
    kit.servo[1].set_pulse_width_range(500, 2500)
    kit.servo[2].set_pulse_width_range(500, 2500)

    kit.servo[0].angle = 0
    kit.servo[1].angle = 0
    kit.servo[2].angle = 0
    time.sleep(2)

    leg = LegIK(20, 0, 80, 80)
    body = BodyIK(160, 110)

    InitialLegPoints = np.array(
        [
            [100, -100, 75, 1],
            [100, -100, -75, 1],
            [-100, -100, 75, 1],
            [-100, -100, -75, 1],
        ]
    )
    reset_body(leg, body, InitialLegPoints)
    (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
    (Lf, _, _, _) = JointAnglesProvider(leg, Tlf, Trf, Tlb, Trb, InitialLegPoints)
    theta1, theta2, theta3 = Lf
    # print(degrees(theta1, degrees(theta2), degrees(theta3))
    # test_on_the_leg(degrees(theta1), degrees(theta2), degrees(theta3), kit)


def test_on_the_leg(theta1, theta2, theta3, kit):
    # Test with 0 degrees and rotation direction
    kit.servo[0].angle = servo_mapping(theta1)
    kit.servo[1].angle = servo_mapping(theta2)
    # output should never be negative or larger than 180
    kit.servo[2].angle = servo_flip(theta3)


def to_deg(theta1, theta2, theta3):
    """
    Change the output from leg IK from radians to degrees.
    """
    return (degrees(theta1), degrees(theta2), degrees(theta3))


def servo_flip(angle):
    """
    Flips the direction that the servo moves in.
    """
    return 180 - angle


def servo_mapping(angle):
    """
    Maps the output from the leg IK to an input usable by the 180degree servo's.
    -90 to 90 -> 0 to 180
    """
    return angle + 90


if __name__ == "__main__":
    main()
