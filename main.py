import time
import numpy as np
import rerun as rr
from motion.walking_engine import WalkingEngine
import argparse


def init_rerun():
    rr.init("Quad-EX visualization")
    rr.connect_tcp("127.0.0.1:9876")


def parse_args():
    parser = argparse.ArgumentParser(description="Quad-EX CLI")
    parser.add_argument(
        "--rerun",
        default=False,
        type=bool,
        help="Flag for enabling rerun. Default set to False.",
    )
    parser.add_argument(
        "--controller",
        default=False,
        type=bool,
        help="Flag that can be enabled if you want to control the robot with a PS4 controller.",
    )
    parser.add_argument(
        "--no_motors",
        default=False,
        type=bool,
        help="Flag that can be turned on if you only want visualization"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.rerun:
        init_rerun()

    # TODO clearly document where the body dimensions come from
    (l1, l2, l3, l4) = (20, 0, 80, 80)
    (length, width) = (160, 110)
    # The LegPoints matrix is the position of the foot relative to the body center (0, 0, 0)
    LegPoints = np.array(
        [
            [100, -100, 75, 1],  # LF
            [100, -100, -75, 1],  # RF
            [-100, -100, 75, 1],  # LB
            [-100, -100, -75, 1],  # RB
        ]
    )
    we = WalkingEngine(l1, l2, l3, l4, length, width, LegPoints, args)
    we.reset_body()
    we.init_walk()

    interval = 0.030
    startTime = time.time()
    lastTime = startTime
    # main control loop
    while True:
        if time.time() - lastTime >= interval:
            loopTime = time.time() - lastTime
            lastTime = time.time()
            t = time.time() - startTime
            we.walk()


if __name__ == "__main__":
    main()