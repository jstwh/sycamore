from evdev import InputDevice, categorize, ecodes
# import evdev
# from select import select #not needed; only for multiple controllers
import numpy as np # for creating L3 and R3 array (joysticks)

# path to controller, found by running the code lines below
controller_path = '/dev/input/event6'

# checking whether controller is connected and can be found
try:
    # code lines below give the path to the controller
        # if these lines are run; uncomment line 2
    # devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # for device in devices:
    #     print(device.path, device.name, device.phys)
    # controller = InputDevice(evdev.list_devices()[0]) # if there is only one
    controller = InputDevice(controller_path)
    print(f"Connected controller: {controller.name}, found at {controller_path}")
except FileNotFoundError:
    print(f"Controller not connected, or not found at {controller_path}")
    exit()


# for-loop for reading events
print("Waiting for a d-pad button to be pressed... Press Ctrl+C to exit.")
for event in controller.read_loop():

    # EV_ABS for joysticks and d-pad
    if event.type == ecodes.EV_ABS:

        # ABS_HAT0X for horizontal movement: d-pad (left/right; x-axis)
        if event.code == ecodes.ABS_HAT0X:
            if event.value == 1:
                print("D-pad arrow pressed: right")
            elif event.value == -1:
                print("D-pad arrow pressed: left")
            elif event.value == 0:
                print("D-pad arrow released")
        
        # ABS_HAT0Y for vertical movement: d-pad (up/down; y-axis)
        if event.code == ecodes.ABS_HAT0Y:
            if event.value == 1:
                print("D-pad arrow pressed: down")
            if event.value == -1:
                print("D-pad arrow pressed: up")
            if event.value == 0:
                print("D-pad arrow released")

            


