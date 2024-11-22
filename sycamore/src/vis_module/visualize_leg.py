import numpy as np
import matplotlib.pyplot as plt
from pynput import keyboard
from queue import Queue
from leg_ik import Leg

# Robot leg parameters
l1 = 100
l2 = 100
x = 0
y = -140
upper = ([], [])
lower = ([], [])
leg = Leg(l1, l2)

# Plot setup
fig = plt.figure()
axis = plt.axes(xlim=(-l1 - l2, l1 + l2), ylim=(-l1 - l2, l1 + l2))
plt.xlabel("X")
plt.ylabel("Y")
plt.grid()
plt.gca().set_aspect("equal")
line1, = axis.plot([], [], lw=2)
line2, = axis.plot([], [], lw=2)

# Communication queue for thread-safe updates
command_queue = Queue()

def update_plot():
    """Update the plot with the current leg position."""
    global upper, lower, t1, t2

    t1 = np.radians(t1)
    t2 = np.radians(t2)

    x0, y0 = 0, 0

    # Forward kinematics
    x1 = l1 * np.cos(t1)
    y1 = l1 * np.sin(t1)

    x2 = x1 + l2 * np.cos(t1 + t2)
    y2 = y1 + l2 * np.sin(t1 + t2)

    upper = ([x0, x1], [y0, y1])
    lower = ([x1, x2], [y1, y2])
    line1.set_data(upper)
    line2.set_data(lower)
    fig.canvas.draw()

def update_pos():
    """Calculate joint angles and positions."""
    global x, y, t1, t2
    t1, t2 = leg.ja_from_xy(x, y)
    leg.xy_from_ja(t1, t2)

def on_press(key):
    """Handle keyboard input and enqueue commands."""
    global x, y
    try:
        if key.char == "w":
            command_queue.put(("move", 0, 5))
        elif key.char == "a":
            command_queue.put(("move", -5, 0))
        elif key.char == "s":
            command_queue.put(("move", 0, -5))
        elif key.char == "d":
            command_queue.put(("move", 5, 0))
    except AttributeError:
        pass

# Start the keyboard listener
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Main update loop
while plt.fignum_exists(fig.number):
    while not command_queue.empty():
        command = command_queue.get()
        if command[0] == "move":
            dx, dy = command[1], command[2]
            x += dx
            y += dy
            update_pos()
            update_plot()
    plt.pause(0.05)

listener.stop()
