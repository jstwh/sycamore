from adafruit_servokit import ServoKit
from ik import LegIK
from math import degrees


def main():
    kit = ServoKit(channels=16)
    kit.servo[0].set_pulse_width_range(500, 2500)
    kit.servo[0].set_pulse_width_range(500, 2500)
    kit.servo[0].set_pulse_width_range(500, 2500)

    # Attach something at 0 angle

    # theta 1
    kit.servo[0].angle = 0
    # theta 2
    kit.servo[1].angle = 0
    # theta 3
    kit.servo[2].angle = 0

    l1 = 56
    l2 = 1
    l3 = 151
    l4 = 176
    leg = LegIK(l1, l2, l3, l4)
    # default-ish position
    (theta1, theta2, theta3) = to_deg(leg.ik(210, -200, 110))
    if theta3 < 0 or theta3 > 180:
        raise ValueError
    # test_on_the_leg(theta1, theta2, theta3, kit)


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
