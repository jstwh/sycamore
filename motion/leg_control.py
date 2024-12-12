from pynput import keyboard
from ik import LegIK
from leg_ik import Leg
from adafruit_servokit import ServoKit
import rerun as rr
import argparse
import math


def main():
    global x, y, z, leg_2, leg_3, args, kit
    args = parse_args()

    # TODO This needs testing on the real leg!
    if args.irl:
        kit = ServoKit(channels=16)
        kit.servo[0].set_pulse_width_range(500, 2500)
        kit.servo[1].set_pulse_width_range(500, 2500)

    if args.rerun:
        rr.init("IK visualization")
        rr.connect_tcp("127.0.0.1:9876")

    l1 = 0.4
    l2 = 0.4
    l3 = 0.05
    x = -0.05
    y = -0.55
    z = 0
    leg_2 = Leg(l1, l2)
    leg_3 = LegIK(l1, l2, l3)

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def update_pos():
    global x, y, z
    t1, t2, t3 = leg_3.ik((x, y, z), "right")
    upper, lower = leg_2.xy_from_ja(math.degrees(t2), math.degrees(t3))

    if args.irl:
        kit.servo[0].angle = t1
        kit.servo[1].angle = t2

    if args.rerun:
        rr.log(
            "leg_data",
            rr.LineStrips3D(
                [upper, lower],
                colors=[[255, 0, 0], [0, 255, 0]],
                labels=["upper leg", "lower leg"],
            ),
        )


def on_press(key):
    global x, y
    print("Press w, a, s, d")
    try:
        if key.char == "w":
            y += 5
        elif key.char == "a":
            x -= 5
        elif key.char == "s":
            y -= 5
        elif key.char == "d":
            x += 5
        else:
            print("Invalid input")
        update_pos()

    except AttributeError:
        print(f"Error: special key {key} pressed")


def parse_args():
    parser = argparse.ArgumentParser(description="Control CLI")
    parser.add_argument(
        "--rerun",
        default=False,
        type=bool,
        help="Flag for enabling rerun. Default set to False.",
    )
    parser.add_argument(
        "--irl",
        default=False,
        type=bool,
        help="Flag that can be enabled if the code should work on the real world leg. Default set to False.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
