from adafruit_servokit import ServoKit
import time
import numpy as np
from motion.ik import BodyIK, LegIK
from motion.step_planner import TrotGait
from visualize import reset_body, draw_robot
from math import radians, degrees
import rerun as rr
from motion.utils import JointAnglesProvider


def main():
    rr.init("IK visualization")
    rr.connect_tcp("145.109.45.135:9876")
    kit = ServoKit(channels=16)

    # Left Front, in order: theta1, theta2, theta3
    kit.servo[0].set_pulse_width_range(500, 2500)  # Shoulder
    kit.servo[1].set_pulse_width_range(500, 2500)  # Upper
    kit.servo[2].set_pulse_width_range(500, 2500)  # Lower
    # Left Back, in order: theta1, theta2, theta3
    kit.servo[3].set_pulse_width_range(500, 2500)  # Shoulder
    kit.servo[4].set_pulse_width_range(500, 2500)  # Upper
    kit.servo[5].set_pulse_width_range(500, 2500)  # Lower
    # Right Front, in order: theta1, theta2, theta3
    kit.servo[6].set_pulse_width_range(500, 2500)  # Shoulder
    kit.servo[7].set_pulse_width_range(500, 2500)  # Upper
    kit.servo[8].set_pulse_width_range(500, 2500)  # Lower
    # Right Back, in order: theta1, theta2, theta3
    kit.servo[9].set_pulse_width_range(500, 2500)  # Shoulder
    kit.servo[10].set_pulse_width_range(500, 2500)  # Upper
    kit.servo[11].set_pulse_width_range(500, 2500)  # Lower

    kit.servo[0].angle = 0
    kit.servo[1].angle = 180
    kit.servo[2].angle = 0
    kit.servo[3].angle = 0
    kit.servo[4].angle = 180
    kit.servo[5].angle = 0
    kit.servo[6].angle = 0
    kit.servo[7].angle = 0
    kit.servo[8].angle = 180
    kit.servo[9].angle = 0
    kit.servo[10].angle = 0
    kit.servo[11].angle = 180
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
    # (Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
    # (Lf, Lb, Rf, Rb) = JointAnglesProvider(leg, Tlf, Trf, Tlb, Trb, InitialLegPoints)
    # test_on_the_leg(Lf, Lb, Rf, Rb, kit)


def test_on_the_leg(Lf, Lb, Rf, Rb, kit):
    Lf = to_deg(Lf)
    Lb = to_deg(Lb)
    Rf = to_deg(Rf)
    Rb = to_deg(Rb)
    # LF
    kit.servo[0].angle = servo_mapping(Lf[0])
    kit.servo[1].angle = servo_flip(servo_mapping(Lf[1]))
    kit.servo[2].angle = servo_flip(Lf[2])
    # LB
    kit.servo[3].angle = servo_mapping(Lb[0])
    kit.servo[4].angle = servo_flip(servo_mapping(Lb[1]))
    kit.servo[5].angle = servo_flip(Lb[2])
    # RF
    kit.servo[6].angle = servo_mapping(Rf[0])
    kit.servo[7].angle = servo_mapping(Rf[1])
    kit.servo[8].angle = servo_flip(Rf[2])
    # RB
    kit.servo[9].angle = servo_mapping(Rb[0])
    kit.servo[10].angle = servo_mapping(Rb[1])
    kit.servo[11].angle = servo_flip(Rb[2])


def to_deg(leg_angles):
    """
    Change the output from leg IK from radians to degrees.
    """
    return (degrees(leg_angles[0]), degrees(leg_angles[1]), degrees(leg_angles[2]))


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
