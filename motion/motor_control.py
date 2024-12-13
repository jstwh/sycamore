from adafruit_servokit import ServoKit


class ServoFactory:
    def __init__(self):
        self.kit = ServoKit(channels=16)
        # Left Front, in order: theta1, theta2, theta3
        self.kit.servo[0].set_pulse_width_range(500, 2500)
        self.kit.servo[1].set_pulse_width_range(500, 2500)
        self.kit.servo[2].set_pulse_width_range(500, 2500)
        # Left Back, in order: theta1, theta2, theta3
        self.kit.servo[3].set_pulse_width_range(500, 2500)
        self.kit.servo[4].set_pulse_width_range(500, 2500)
        self.kit.servo[5].set_pulse_width_range(500, 2500)
        # Right Front, in order: theta1, theta2, theta3
        self.kit.servo[6].set_pulse_width_range(500, 2500)
        self.kit.servo[7].set_pulse_width_range(500, 2500)
        self.kit.servo[8].set_pulse_width_range(500, 2500)
        # Right Back, in order: theta1, theta2, theta3
        self.kit.servo[9].set_pulse_width_range(500, 2500)
        self.kit.servo[10].set_pulse_width_range(500, 2500)
        self.kit.servo[11].set_pulse_width_range(500, 2500)

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
        self.kit.servo[0].angle = lf[0] + 0
        self.kit.servo[1].angle = lf[1] + 0
        self.kit.servo[2].angle = lf[2] + 0

        self.kit.servo[0].angle = lb[0] + 0
        self.kit.servo[1].angle = lb[1] + 0
        self.kit.servo[2].angle = lb[2] + 0

        self.kit.servo[0].angle = rf[0] + 0
        self.kit.servo[1].angle = rf[1] + 0
        self.kit.servo[2].angle = rf[2] + 0

        self.kit.servo[0].angle = rb[0] + 0
        self.kit.servo[1].angle = rb[1] + 0
        self.kit.servo[2].angle = rb[2] + 0
