from evdev import InputDevice, categorize, ecodes, list_devices
# from select import select #not needed; only for multiple controllers
import numpy as np # for creating L3 and R3 array (joysticks)


# checking whether controller is connected and can be found
try:
    controller = InputDevice('/dev/input/event7')
    # devices = [InputDevice(path) for path in list_devices()]
    # for device in devices:
    #     if 'Controller' in device.name:
    #         controller = device

    # controller = InputDevice(list_devices()[0]) # if there is only one
    print(f"Connected controller: {controller.name}, found at {controller.path}")
except FileNotFoundError:
    # print(f"Controller not connected, or not found at {controller.path}")
    print("Controller not connected, or not found")
    exit()

# defining parameters
x, y = 0, 0
x_wjoy, y_wjoy = 0, 0
position = [x, y]
threshold = 0.1 # for joystick input
step_size = 1

# for-loop for reading events
print("Waiting for a d-pad button to be pressed... Press O-button to exit.")
print(f"location: {position}")

try:
    for event in controller.read_loop():

        # EV_ABS for d-pad and joysticks
        if event.type == ecodes.EV_ABS:

            # ABS_HAT0X for horizontal movement: d-pad (left/right; x-axis)
                # could be coded better
            if event.code == ecodes.ABS_HAT0X:
                if event.value == 1:
                    x += step_size
                    position[0] = x
                    print("D-pad arrow pressed: right")
                    print(f"location coordinates: {position} \n")
                elif event.value == -1:
                    x -= step_size
                    position[0] = x
                    print("D-pad arrow pressed: left")
                    print(f"location coordinates: {position} \n")
                elif event.value == 0:
                    print("D-pad arrow released")
        
            # ABS_HAT0Y for vertical movement: d-pad (up/down; y-axis)
                # could be coded better
            elif event.code == ecodes.ABS_HAT0Y:
                if event.value == 1:
                    y -= step_size
                    position[1] = y
                    print("D-pad arrow pressed: down")
                    print(f"location coordinates: {position} \n")
                elif event.value == -1:
                    y += step_size
                    position[1] = y
                    print("D-pad arrow pressed: up")
                    print(f"location coordinates: {position} \n")
                if event.value == 0:
                    print("D-pad arrow released")

            # NOT TESTED
            # using left joystick to move
# Uncomment section start
            # elif event.code == ecodes.ABS_X:
            #     if event.value >= threshold:
            #         x_wjoy += round(event.value, 2)
# Uncomment section end
                    # use line below if using a step size is the preferred option
                        # adjust step_size in parameter defining section
                    # X_wjoy += step_size * round(event.value, 2)
# Uncomment section start
            # elif event.code == ecodes.ABS_Y:
            #     if event.value >= threshold:
            #         y_wjoy += round(event.value, 2)
# Uncomment section end
                    # use line below if using a step size is preferred
                        # adjust step_size in parameter defining section
                    # y_wjoy += step_size * round(event.value, 2)

            # possibility to program right joystick
# Uncomment section start --
            # elif event.code == ecodes.ABS_RX:
            #     if event.value >= threshold:
            #         pass
            # elif event.code == ecodes.ABS_RY:
            #     if event.value >= threshold:
            #         pass
# -- Uncomment section end
        # triangle, O, X and square button programmed below, change where necessary :)
        
        elif event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_NORTH: # triangle-button pressed
                pass

            # stop program when O-button is pressed
            elif event.code == ecodes.BTN_EAST: # O-button pressed
                print("Exiting...")
                break
            elif event.code == ecodes.BTN_SOUTH: # X-button pressed
                pass
            elif event.code == ecodes.BTN_WEST: # squaree-button pressed
                pass

                
finally:
    # controller.close()
    print("Done!")