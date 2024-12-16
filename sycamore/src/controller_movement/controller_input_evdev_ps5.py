from evdev import InputDevice, categorize, ecodes, list_devices
# from select import select #not needed; only for multiple controllers
import numpy as np # for creating L3 and R3 array (joysticks)


# checking whether controller is connected and can be found
try:

    # devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # for device in devices:
    #     print(device.path, device.name, device.phys)
    controller = InputDevice(list_devices()[0]) # if there is only one
    print(f"Connected controller: {controller.name}, found at {controller.path}")
except FileNotFoundError:
    print(f"Controller not connected, or not found at {controller.path}")
    exit()


# for-loop for reading events
x, y = 0, 0
position = [x, y]
print("Waiting for a d-pad button to be pressed... Press Ctrl+C to exit.")
print(f"location: {position}")

try:
    for event in controller.read_loop():

        # EV_ABS for joysticks and d-pad
        if event.type == ecodes.EV_ABS:

            # ABS_HAT0X for horizontal movement: d-pad (left/right; x-axis)
            if event.code == ecodes.ABS_HAT0X:
                if event.value == 1:
                    x += 1
                    position[0] = x
                    print("D-pad arrow pressed: right")
                    print(f"location coordinates: {position} \n")
                elif event.value == -1:
                    x -= 1
                    position[0] = x
                    print("D-pad arrow pressed: left")
                    print(f"location coordinates: {position} \n")
                elif event.value == 0:
                    print("D-pad arrow released")
        
            # ABS_HAT0Y for vertical movement: d-pad (up/down; y-axis)
            elif event.code == ecodes.ABS_HAT0Y:
                if event.value == 1:
                    y -= 1
                    position[1] = y
                    print("D-pad arrow pressed: down")
                    print(f"location coordinates: {position} \n")
                elif event.value == -1:
                    y += 1
                    position[1] = y
                    print("D-pad arrow pressed: up")
                    print(f"location coordinates: {position} \n")
                if event.value == 0:
                    print("D-pad arrow released")

        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_EAST:
                print("Exiting...")
                break
                
finally:
    controller.close()