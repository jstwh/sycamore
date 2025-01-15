"""
Based on:
    - https://www.researchgate.net/publication/332374021_Leg_Trajectory_Planning_for_Quadruped_Robots_with_High-Speed_Trot_Gait.
    - https://github.com/miguelasd688/4-legged-robot-model
    - https://github.com/pat92fr/FootTrajectoryPlanner
"""

import time
import numpy as np


def f(n, k):
    return np.math.factorial(n) / (np.math.factorial(k) * np.math.factorial(n - k))


def b(t, k, point):
    n = 9
    return point * f(n, k) * np.power(t, k) * np.power(1 - t, n - k)


class TrotGait:
    def __init__(self):
        """
        v -- linear velocity
        angle -- angle in degrees
        w_rot -- rotational velocity
        t -- period of one step
        offset -- phase offsets for each foot
        phi_st -- phase of the stance, between [0,1)
        phi_sw -- phase of the swing, between [0,1)
        """
        self.LegPoints = np.array(
            [
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
            ]
        )
        self.phi = 0.0  # Phase of the gait cycle
        self.phi_stance = 0.0  # Phase of the stance
        self.last_time = time.time()
        self.alpha = 0.0  # Rotation angle
        self.s = False  # Some state variable

    def calculate_stance(self, phi_st, v, angle):
        c = np.cos(np.deg2rad(angle))
        s = np.sin(np.deg2rad(angle))

        a = 0.0005  # Constant for vertical displacement
        half_stance = 0.05  # Half of the stance length
        p_stance = half_stance * (1 - 2 * phi_st)  # Position along the stance

        stance_x = c * p_stance * np.abs(v)
        stance_y = -a * np.cos(np.pi / (2 * half_stance) * p_stance)
        stance_z = -s * p_stance * np.abs(v)

        return stance_x, stance_z, stance_y

    def calculate_bezier_swing(self, phi_sw, v, angle):
        c = np.cos(np.deg2rad(angle))
        s = np.sin(np.deg2rad(angle))

        # Control points for the Bezier curve
        X = (
            np.abs(v)
            * c
            * np.array([-0.05, -0.06, -0.07, -0.07, 0.0, 0.0, 0.07, 0.07, 0.06, 0.05])
        )
        Z = np.abs(v) * np.array(
            [0.0, 0.0, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.0, 0.0]
        )
        # Z = -Z
        Y = (
            np.abs(v)
            * s
            * np.array([0.05, 0.06, 0.07, 0.07, 0.0, -0.0, -0.07, -0.07, -0.06, -0.05])
        )

        swing_x = 0.0
        swing_y = 0.0
        swing_z = 0.0

        for i in range(10):
            swing_x += b(phi_sw, i, X[i])
            swing_y += b(phi_sw, i, Y[i])
            swing_z += b(phi_sw, i, Z[i])

        return swing_x, swing_z, swing_y

    def step_trajectory(self, phi, v, angle, w_rot, LegPoints):
        if phi >= 1:
            phi = phi - 1.0  # Modify phi to be within [0,1) range
        #phi = 1 - phi
        r = np.sqrt(LegPoints[0] ** 2 + LegPoints[1] ** 2)
        foot_angle = np.arctan2(
            LegPoints[1], LegPoints[0]
        )  # Angle of the foot relative to the center

        if w_rot >= 0.0:
            circle_trajectory = 90.0 - np.rad2deg(foot_angle - self.alpha)
        else:
            circle_trajectory = 270.0 - np.rad2deg(foot_angle - self.alpha)

        step_offset = 0.75  # Offset to separate the stance and swing phases
        if phi <= step_offset:  # Stance phase
            phi_stance = phi / step_offset
            step_x_long, step_y_long, step_z_long = self.calculate_stance(
                phi_stance, v, angle
            )
            step_x_rot, step_y_rot, step_z_rot = self.calculate_stance(
                phi_stance, w_rot, circle_trajectory
            )
        else:  # Swing phase
            phi_swing = (phi - step_offset) / (1 - step_offset)
            step_x_long, step_y_long, step_z_long = self.calculate_bezier_swing(
                phi_swing, v, angle
            )
            step_x_rot, step_y_rot, step_z_rot = self.calculate_bezier_swing(
                phi_swing, w_rot, circle_trajectory
            )

        if LegPoints[1] > 0:  # Define the sign for rotation based on foot's position
            if step_x_rot < 0:
                self.alpha = -np.arctan2(np.sqrt(step_x_rot**2 + step_z_rot**2), r)
            else:
                self.alpha = np.arctan2(np.sqrt(step_x_rot**2 + step_z_rot**2), r)
        else:
            if step_x_rot < 0:
                self.alpha = np.arctan2(np.sqrt(step_x_rot**2 + step_z_rot**2), r)
            else:
                self.alpha = -np.arctan2(np.sqrt(step_x_rot**2 + step_z_rot**2), r)

        coord = np.empty(3)
        coord[1] = step_x_long + step_x_rot
        coord[0] = step_y_long + step_y_rot
        coord[2] = step_z_long + step_z_rot

        return coord

    def loop(self, v, angle, w_rot, t, offset, LegPoints):
        # Minimum time period
        if t <= 0.01:
            t = 0.01

        if self.phi >= 0.99:
            self.last_time = time.time()
        self.phi = (time.time() - self.last_time) / t

        step_coord = self.step_trajectory(
            self.phi + offset[0],
            v,
            angle,
            w_rot,
            np.squeeze(np.asarray(LegPoints[0, :-1])),
        )
        self.LegPoints[0, 0] = LegPoints[0, 0] + step_coord[0]
        self.LegPoints[0, 1] = LegPoints[0, 1] + step_coord[1]
        self.LegPoints[0, 2] = LegPoints[0, 2] + step_coord[2]

        step_coord = self.step_trajectory(
            self.phi + offset[1],
            v,
            angle,
            w_rot,
            np.squeeze(np.asarray(LegPoints[1, :-1])),
        )
        self.LegPoints[1, 0] = LegPoints[1, 0] + step_coord[0]
        self.LegPoints[1, 1] = LegPoints[1, 1] + step_coord[1]
        self.LegPoints[1, 2] = LegPoints[1, 2] + step_coord[2]

        step_coord = self.step_trajectory(
            self.phi + offset[2],
            v,
            angle,
            w_rot,
            np.squeeze(np.asarray(LegPoints[2, :-1])),
        )
        self.LegPoints[2, 0] = LegPoints[2, 0] + step_coord[0]
        self.LegPoints[2, 1] = LegPoints[2, 1] + step_coord[1]
        self.LegPoints[2, 2] = LegPoints[2, 2] + step_coord[2]

        step_coord = self.step_trajectory(
            self.phi + offset[3],
            v,
            angle,
            w_rot,
            np.squeeze(np.asarray(LegPoints[3, :-1])),
        )
        self.LegPoints[3, 0] = LegPoints[3, 0] + step_coord[0]
        self.LegPoints[3, 1] = LegPoints[3, 1] + step_coord[1]
        self.LegPoints[3, 2] = LegPoints[3, 2] + step_coord[2]

        return self.LegPoints
