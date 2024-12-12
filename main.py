"""
Contains the main event loop running at ~20hz.
"""
import time
import numpy as np
from motion.ik import BodyIK, LegIK
from motion.step_planner import TrotGait
from motion.visualize import reset_body, init_rerun, draw_robot
from math import radians

init_rerun()
leg = LegIK(20, 0, 80, 80)
body = BodyIK(160, 110)
trot = TrotGait()
startTime = time.time()
lastTime = startTime
"""
The LegPoints matrix is the position of the foot relative to the body center (0, 0, 0):
    - Left Front: LegPoints[0]
    - Right Front: LegPoints[1]
    - Left Back: LegPoints[2]
    - Right Back: LegPoints[3]
"""
InitialLegPoints = np.array(
    [
        [100, -100, 75, 1],
        [100, -100, -75, 1],
        [-100, -100, 75, 1],
        [-100, -100, -75, 1],
    ]
)
reset_body(leg, body, InitialLegPoints)
T = 1.0
offset = np.array([0. , 0.5 , 0.5 , 0.])
(Tlf, Trf, Tlb, Trb, Tm) = body.ik(radians(0), radians(0), radians(0), 0, 0, 0)
interval = 0.030

while(True):
    if (time.time()-lastTime >= interval):
        loopTime = time.time() - lastTime
        lastTime = time.time()
        t = time.time() - startTime
        LegPoints = trot.loop(200, 0, 0, T, offset, InitialLegPoints)
        draw_robot(leg, body, (Tlf, Trf, Tlb, Trb, Tm), LegPoints)
