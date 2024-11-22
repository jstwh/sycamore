from pynput import keyboard
from leg_ik import Leg

l1 = 100
l2 = 100
x = 0
y = 140
leg = Leg(l1, l2)

def update_pos():
    global x, y
    t1, t2 = leg.ja_from_xy(x, y)
    leg.xy_from_ja(t1, t2)

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

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events untill released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()