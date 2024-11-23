from pynput import keyboard
from leg_ik import Leg
import numpy as np
import rerun as rr
import rerun.blueprint as rrb

rr.init("rerun_leg_example", spawn=True)

l1 = 100
l2 = 100
x = 0
y = -140
leg = Leg(l1, l2)
upper = [[], []]
lower = [[], []]

def update_pos():
    global x, y, coords
    t1, t2 = leg.ja_from_xy(x, y)
    upper, lower = leg.xy_from_ja(t1, t2)

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

# Set view bounds:
#rr.send_blueprint(rrb.Spatial3DView(visual_bounds=rrb.VisualBounds3D(x_range=[-l1-l2, l1+l2], y_range=[-l1-l2, l1+l2], z_range=[10, -10])))

with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
