from adafruit_servokit import ServoKit
from math import degrees


class ServoFactory:
    def __init__(self):
        self.kit0 = ServoKit(channels=16, address=0x42)
        self.kit1 = ServoKit(channels=16, address=0x44)
        # Left Front, in order: theta1, theta2, theta3
        self.kit0.servo[0].set_pulse_width_range(500, 2500)
        self.kit0.servo[1].set_pulse_width_range(500, 2500)
        self.kit0.servo[2].set_pulse_width_range(500, 2500)
        # Left Back, in order: theta1, theta2, theta3
        self.kit0.servo[3].set_pulse_width_range(500, 2500)
        self.kit0.servo[4].set_pulse_width_range(500, 2500)
        self.kit0.servo[5].set_pulse_width_range(500, 2500)
        # Right Front, in order: theta1, theta2, theta3
        self.kit1.servo[6].set_pulse_width_range(500, 2500)
        self.kit1.servo[7].set_pulse_width_range(500, 2500)
        self.kit1.servo[8].set_pulse_width_range(500, 2500)
        # Right Back, in order: theta1, theta2, theta3
        self.kit1.servo[9].set_pulse_width_range(500, 2500)
        self.kit1.servo[10].set_pulse_width_range(500, 2500)
        self.kit1.servo[11].set_pulse_width_range(500, 2500)

    def move_servos(self, lf: tuple, lb: tuple, rf: tuple, rb: tuple):
        """
        Provided a tuple containing (theta1, theta2, theta3) from the inverse kinematics for each
        leg, move the servos.

        There is an offset for each servo, this is based on the fact that the zero position of the
        servo is different from the zero position of the actual leg attached. This offset occurs
        because the little metal gear that you attach the servo arm to will force you to have an
        offset in the arm which causes it to be close but not perfectly equal to the position. If
        the legs get de-assembled or changed this will have to be done manually again to figure out
        the new offsets.
        """
        Lf = to_deg(lf)
        Lb = to_deg(lb)
        Rf = to_deg(rf)
        Rb = to_deg(rb)
        # LF
        self.kit0.servo[0].angle = servo_mapping(Lf[0]) + 25
        self.kit0.servo[1].angle = servo_flip(servo_mapping(Lf[1]) - 15)
        self.kit0.servo[2].angle = Lf[2] + 20
        # LB
        self.kit0.servo[3].angle = servo_flip(servo_mapping(Lb[0]) - 15)
        self.kit0.servo[4].angle = servo_flip(servo_mapping(Lb[1]) - 16)
        self.kit0.servo[5].angle = Lb[2] + 8
        # RF
        self.kit1.servo[6].angle = servo_flip(servo_mapping(Rf[0]) - 15)
        self.kit1.servo[7].angle = servo_mapping(Rf[1] - 5)
        self.kit1.servo[8].angle = servo_flip(Rf[2] - 10)
        # RB
        self.kit1.servo[9].angle = servo_mapping(Rb[0]) + 4
        self.kit1.servo[10].angle = servo_mapping(Rb[1]) + 10
        self.kit1.servo[11].angle = servo_flip(Rb[2]) + 5


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
