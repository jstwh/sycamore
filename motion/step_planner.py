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
        V -- linear velocity
        angle -- angle in degrees
        Wrot -- rotational velocity
        T -- period of one step
        offset -- phase offsets for each foot
        phi_st -- phase of the stance, between [0,1)
        phi_sw -- phase of the swing, between [0,1)
        """
        self.bodytoFeet = np.array(
            [
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
                [0, 0, 0, 1],
            ]
        )
        self.phi = 0.0  # Phase of the gait cycle
        self.phi_stance = 0.0  # Phase of the stance
        self.last_time = time.time()  # Last update time
        self.alpha = 0.0  # Rotation angle
        self.s = False  # Some state variable

    def calculate_stance(self, phi_st, v, angle):
        c = np.cos(np.deg2rad(angle))  # Cosine of the angle in radians
        s = np.sin(np.deg2rad(angle))  # Sine of the angle in radians

        a = 0.0005  # Constant for vertical displacement
        half_stance = 0.05  # Half of the stance length
        p_stance = half_stance * (1 - 2 * phi_st)  # Position along the stance

        stance_x = c * p_stance * np.abs(v)  # X position
        stance_y = -s * p_stance * np.abs(v)  # Y position
        stance_z = -a * np.cos(np.pi / (2 * half_stance) * p_stance)  # Z position

        return stance_x, stance_y, stance_z

    def calculateBezier_swing(self, phi_sw, v, angle):
        c = np.cos(np.deg2rad(angle))  # Cosine of the angle in radians
        s = np.sin(np.deg2rad(angle))  # Sine of the angle in radians

        # Control points for the Bezier curve
        X = (np.abs(v) * c * np.array([-0.05, -0.06, -0.07, -0.07, 0.0, 0.0, 0.07, 0.07, 0.06, 0.05]))
        Y = (np.abs(v) * s * np.array([0.05, 0.06, 0.07, 0.07, 0.0, -0.0, -0.07, -0.07, -0.06, -0.05]))
        Z = np.abs(v) * np.array([0.0, 0.0, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.0, 0.0])

        # Initialize the swing positions
        swing_x = 0.0
        swing_y = 0.0
        swing_z = 0.0

        # Sum all terms of the Bezier curve
        for i in range(10):
            swing_x = swing_x + b(phi_sw, i, X[i])
            swing_y = swing_y + b(phi_sw, i, Y[i])
            swing_z = swing_z + b(phi_sw, i, Z[i])

        return swing_x, swing_y, swing_z

    def stepTrajectory(self, phi, V, angle, Wrot, centerToFoot):
        if phi >= 1:
            phi = phi - 1.0  # Modify phi to be within [0,1) range
        r = np.sqrt(centerToFoot[0] ** 2 + centerToFoot[1] ** 2)  # Radius of the circumscribed circle
        footAngle = np.arctan2(centerToFoot[1], centerToFoot[0])  # Angle of the foot relative to the center

        if Wrot >= 0.0:
            circleTrayectory = 90.0 - np.rad2deg(footAngle - self.alpha)
        else:
            circleTrayectory = 270.0 - np.rad2deg(footAngle - self.alpha)

        stepOffset = 0.75  # Offset to separate the stance and swing phases
        if phi <= stepOffset:  # Stance phase
            phiStance = phi / stepOffset
            stepX_long, stepY_long, stepZ_long = self.calculate_stance(phiStance, V, angle)
            stepX_rot, stepY_rot, stepZ_rot = self.calculate_stance(phiStance, Wrot, circleTrayectory)
        else:  # Swing phase
            phiSwing = (phi - stepOffset) / (1 - stepOffset)
            stepX_long, stepY_long, stepZ_long = self.calculateBezier_swing(phiSwing, V, angle)
            stepX_rot, stepY_rot, stepZ_rot = self.calculateBezier_swing(phiSwing, Wrot, circleTrayectory)

        if centerToFoot[1] > 0:  # Define the sign for rotation based on foot's position
            if stepX_rot < 0:
                self.alpha = -np.arctan2(np.sqrt(stepX_rot**2 + stepY_rot**2), r)
            else:
                self.alpha = np.arctan2(np.sqrt(stepX_rot**2 + stepY_rot**2), r)
        else:
            if stepX_rot < 0:
                self.alpha = np.arctan2(np.sqrt(stepX_rot**2 + stepY_rot**2), r)
            else:
                self.alpha = -np.arctan2(np.sqrt(stepX_rot**2 + stepY_rot**2), r)

        coord = np.empty(3)  # Initialize coordinates array
        coord[0] = stepX_long + stepX_rot  # Final X position
        coord[1] = stepY_long + stepY_rot  # Final Y position
        coord[2] = stepZ_long + stepZ_rot  # Final Z position

        return coord

    def loop(self, V, angle, Wrot, T, offset, LegPoints):
        if T <= 0.01:
            T = 0.01  # Minimum time period

        if self.phi >= 0.99:  # Update lastTime if phase exceeds 0.99
            self.last_time = time.time()
        self.phi = (time.time() - self.last_time) / T  # Compute current phase of the gait cycle
    
        # Calculate trajectory for each foot separately
        step_coord = self.stepTrajectory(self.phi + offset[0], V, angle, Wrot, np.squeeze(np.asarray(LegPoints[0, :-1])))
        self.bodytoFeet[0, 0] = LegPoints[0, 0] + step_coord[0]
        self.bodytoFeet[0, 1] = LegPoints[0, 1] + step_coord[1]
        self.bodytoFeet[0, 2] = LegPoints[0, 2] + step_coord[2]
        print(step_coord[2])
        print(self.bodytoFeet[0, 2])

        step_coord = self.stepTrajectory(self.phi + offset[1], V, angle, Wrot, np.squeeze(np.asarray(LegPoints[1, :-1])))
        self.bodytoFeet[1, 0] = LegPoints[1, 0] + step_coord[0]
        self.bodytoFeet[1, 1] = LegPoints[1, 1] + step_coord[1]
        self.bodytoFeet[1, 2] = LegPoints[1, 2] + step_coord[2]

        step_coord = self.stepTrajectory(self.phi + offset[2], V, angle, Wrot, np.squeeze(np.asarray(LegPoints[2, :-1])))
        self.bodytoFeet[2, 0] = LegPoints[2, 0] + step_coord[0]
        self.bodytoFeet[2, 1] = LegPoints[2, 1] + step_coord[1]
        self.bodytoFeet[2, 2] = LegPoints[2, 2] + step_coord[2]

        step_coord = self.stepTrajectory(self.phi + offset[3], V, angle, Wrot, np.squeeze(np.asarray(LegPoints[3, :-1])))
        self.bodytoFeet[3, 0] = LegPoints[3, 0] + step_coord[0]
        self.bodytoFeet[3, 1] = LegPoints[3, 1] + step_coord[1]
        self.bodytoFeet[3, 2] = LegPoints[3, 2] + step_coord[2]

        return self.bodytoFeet
