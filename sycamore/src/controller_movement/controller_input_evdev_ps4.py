from evdev import InputDevice, categorize, ecodes
import evdev
# from select import select #not needed; only for multiple controllers
import numpy as np

# path to controller, found by running the code lines below
controller_path = '/dev/input/event6'

# checking whether controller is connected and can be found
try:
    # code lines below give the path to the controller
    # devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    # for device in devices:
    #     print(device.path, device.name, device.phys)
    # controller = InputDevice(evdev.list_devices()[0]) # if there is only one
    controller = InputDevice(controller_path)
    print(f"Connected controller: {controller.name}, found at {controller_path}")
except FileNotFoundError:
    print(f"Controller not connected, or not found at {controller_path}")
    exit()

