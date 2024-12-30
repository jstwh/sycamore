from motion.ik import BodyIK, LegIK
from motion.motor_control import ServoFactory
from math import radians
from motion.utils import JointAnglesProvider
import numpy as np
from motion.step_planner import TrotGait
from motion.visualize import draw_robot


class WalkingEngine:
    def __init__(self, l1, l2, l3, l4, length, width, LegPoints, args):
        self.args = args
        self.leg = LegIK(l1, l2, l3, l4)
        self.body = BodyIK(length, width)
        self.LegPoints = LegPoints
        self.CurrentLegPoints = LegPoints
        if args.no_motors == False:
            self.servo_factory = ServoFactory()

    def reset_body(self):
        (Tlf, Trf, Tlb, Trb, Tm) = self.body.ik(
            radians(0), radians(0), radians(0), 0, 0, 0
        )
        if self.args.no_motors == False:
            (lf, lb, rf, rb) = JointAnglesProvider(
                self.leg, Tlf, Trf, Tlb, Trb, self.LegPoints
            )
            self.servo_factory.move_servos(lf, lb, rf, rb)
        if self.args.rerun:
            draw_robot(self.leg, self.body, (Tlf, Trf, Tlb, Trb, Tm), self.LegPoints)
    
    def init_walk(self, gait="trot"):
        if gait == "trot":
            self.gait = TrotGait()
            self.T = self.body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
            self.offset = np.array([0.0, 0.5, 0.5, 0.0])


    def walk(self, t=0.8, v=250, angle=0, w_rot=0):
        if self.gait is None:
            raise ValueError("Gait not initialized. Call init_walk first.")

        if isinstance(self.gait, TrotGait):
            (Tlf, Trf, Tlb, Trb, Tm) = self.T
            self.CurrentLegPoints = self.gait.loop(v, angle, w_rot, t, self.offset, self.LegPoints)
            if self.args.no_motors == False:
                (lf, lb, rf, rb) = JointAnglesProvider(
                    self.leg, Tlf, Trf, Tlb, Trb, self.CurrentLegPoints
                )
                self.servo_factory.move_servos(lf, lb, rf, rb)
            if self.args.rerun:
                draw_robot(self.leg, self.body, (Tlf, Trf, Tlb, Trb, Tm), self.CurrentLegPoints)