from motion.ik import BodyIK, LegIK
from motion.motor_control import ServoFactory
from math import radians
from motion.utils import JointAnglesProvider
import numpy as np
from motion.step_planner import TrotGait
from visualize import draw_robot


class WalkingEngine:
    def __init__(self, l1, l2, l3, l4, length, width, LegPoints, args):
        self.args = args
        self.leg = LegIK(l1, l2, l3, l4)
        self.body = BodyIK(length, width)
        self.LegPoints = LegPoints
        self.CurrentLegPoints = LegPoints

        if args.motors == True:
            self.servo_factory = ServoFactory()

    def reset_body(self):
        (Tlf, Trf, Tlb, Trb, Tm) = self.body.ik(
            radians(10), radians(0), radians(0), 0, 0, 0
        )
        if self.args.motors == True:
            (lf, lb, rf, rb) = JointAnglesProvider(
                self.leg, Tlf, Trf, Tlb, Trb, self.LegPoints
            )
            self.servo_factory.move_servos(lf, lb, rf, rb)
        if self.args.rerun:
            draw_robot(self.leg, self.body, (Tlf, Trf, Tlb, Trb, Tm), self.LegPoints)

    def init_walk(self, gait="trot"):
        if gait == "trot":
            self.gait = TrotGait()
            self.T = self.body.ik(radians(10), radians(0), radians(0), 0, 0, 0)
            self.offset = np.array([0.0, 0.5, 0.5, 0.0])

    def walk(self, direction="forward"):
        self.direction = direction

        if self.gait is None:
            raise ValueError("Gait not initialized. Call init_walk first.")

        if isinstance(self.gait, TrotGait):
            (Tlf, Trf, Tlb, Trb, Tm) = self.T
            # if self.direction == "forward":
            #     self.CurrentLegPoints = self.gait.loop(
            #         950, 0, 0, 0.4, self.offset, self.LegPoints
            #     )
            # elif self.direction == "left":
            #     self.CurrentLegPoints = self.gait.loop(
            #         0, -90, 950, 0.4, self.offset, self.LegPoints
            #     )
            # elif self.direction == "right":
            #     self.CurrentLegPoints = self.gait.loop(
            #         0, 90, 950, 0.4, self.offset, self.LegPoints
            #     )
            # else:
            #     raise ValueError("Invalid direction specified.")

            self.CurrentLegPoints = self.gait.loop(
                    1000, 0, 0, 0.8, self.offset, self.LegPoints
                )
            # self.CurrentLegPoints = self.gait.loop(
            #     0, -90, 1000, 0.8, self.offset, self.LegPoints
            # )

            if self.args.motors == True:
                (lf, lb, rf, rb) = JointAnglesProvider(
                    self.leg, Tlf, Trf, Tlb, Trb, self.CurrentLegPoints
                )
                self.servo_factory.move_servos(lf, lb, rf, rb)
            if self.args.rerun:
                draw_robot(
                    self.leg, self.body, (Tlf, Trf, Tlb, Trb, Tm), self.CurrentLegPoints
                )

    def walk_with_controller(self, v, angle, w_rot):
        if self.gait is None:
            raise ValueError("Gait not initialized. Call init_walk first.")

        if isinstance(self.gait, TrotGait):
            (Tlf, Trf, Tlb, Trb, Tm) = self.T
            self.CurrentLegPoints = self.gait.loop(
                v, angle, w_rot, 0.8, self.offset, self.LegPoints
            )

            if self.args.motors == True:
                (lf, lb, rf, rb) = JointAnglesProvider(
                    self.leg, Tlf, Trf, Tlb, Trb, self.CurrentLegPoints
                )
                self.servo_factory.move_servos(lf, lb, rf, rb)
            if self.args.rerun:
                draw_robot(
                    self.leg, self.body, (Tlf, Trf, Tlb, Trb, Tm), self.CurrentLegPoints
                )

    def init_twerk(self):
        tw = [-60, -60, -60, -60, -60, -80, -80, -80, -80, -80, -100, -120, -140, -140, -120, -100, -80, -60]
        self.twerk_array = []
        self.twerk_array.extend(tw * 50)
        self.T = self.body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
        self.twerk_idx = 0

    def twerk(self):
        """
        -x
            |
            |
            |    /  z
            |   /
            |  /
            | /
            |/____________  -y
        """
        self.CurrentLegPoints[0][0] = 20
        self.CurrentLegPoints[1][0] = 20
        self.CurrentLegPoints[2][0] = self.twerk_array[self.twerk_idx]
        self.CurrentLegPoints[3][0] = self.twerk_array[self.twerk_idx]

        self.twerk_idx += 1

        (Tlf, Trf, Tlb, Trb, _) = self.T
        if self.args.motors == True:
            (lf, lb, rf, rb) = JointAnglesProvider(
                self.leg, Tlf, Trf, Tlb, Trb, self.CurrentLegPoints
            )
            self.servo_factory.move_servos(lf, lb, rf, rb)