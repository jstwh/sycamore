import time
import numpy as np
import rerun as rr
from motion.walking_engine import WalkingEngine
import argparse
import serial
from sensors.lcd import display_ip, get_ip, send_ip_to_arduino
from sensors.distance import DistanceReader
from motion.ps4 import Controller


PORT = "/dev/ttyACM0"
BAUDRATE = 9600


def init_rerun():
    rr.init("Quad-EX visualization")
    rr.connect_tcp("145.109.52.77:9876")


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
        help="Flag that can be turned on if you only want visualization",
    )
    parser.add_argument(
        "--arduino",
        default=True,
        type=bool,
        help="Flag that can be disabled if not using an arduino.",
    )
    return parser.parse_args()


def main_control_loop(we, distance_reader, args):
    interval = 0.030
    startTime = time.time()
    lastTime = startTime

    while True:
        if time.time() - lastTime >= interval:
            loopTime = time.time() - lastTime
            lastTime = time.time()
            t = time.time() - startTime

            if args.controller:
                controller = Controller()
                v, angle, w_rot = controller.read()
                we.walk_with_controller(v, angle, w_rot)

            else:
                # Give the arduino time to send over serial
                if args.arduino and distance_reader.left:
                    left = distance_reader.left
                    right = distance_reader.right

                    if left < 30 and right < 30:
                        we.walk(direction="left")
                    elif left < 30 and right > 30:
                        we.walk(direction="left")
                    elif left > 30 and right < 30:
                        we.walk(direction="right")
                    else:
                        we.walk(direction="forward")
                else:
                    we.walk(direction="forward")


if __name__ == "__main__":
    args = parse_args()

    if args.arduino:
        ser = serial.Serial(PORT, BAUDRATE, timeout=0.5)
        display_ip(ser)

    if args.rerun:
        init_rerun()

    # # TODO clearly document where the body dimensions come from
    # (l1, l2, l3, l4) = (20, 0, 80, 80)
    # (length, width) = (160, 110)
    # # The LegPoints matrix is the position of the foot relative to the body center (0, 0, 0)
    # LegPoints = np.array(
    #     [
    #         [100, -100, 75, 1],  # LF
    #         [100, -100, -75, 1],  # RF
    #         [-100, -100, 75, 1],  # LB
    #         [-100, -100, -75, 1],  # RB
    #     ]
    # )

    l1 = 56
    l2 = 1
    l3 = 151
    l4 = 176
    length = 420
    width = 220
    LegPoints = np.array(
        [
            [180, -220, 166, 1],
            [180, -220, -166, 1],
            [-180, -220, 166, 1],
            [-180, -220, -166, 1],
        ]
    )
    we = WalkingEngine(l1, l2, l3, l4, length, width, LegPoints, args)
    we.reset_body()
    we.init_walk()

    if args.arduino:
        # ser = serial.Serial(PORT, BAUDRATE, timeout=0.5)
        distance_reader = DistanceReader(ser)
        distance_reader.start()

        try:
            main_control_loop(we, distance_reader, args)
        except KeyboardInterrupt:
            distance_reader.stop()
            distance_reader.join()
            ser.close()
    else:
        main_control_loop()
