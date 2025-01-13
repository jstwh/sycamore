from evdev import InputDevice
import numpy as np

class Controller:
    def __init__(self):
        try:
            self.controller = InputDevice('/dev/input/event7')
            print(f"Connected controller: {self.controller.name}, found at {self.controller.path}")
        except FileNotFoundError:
            print("Controller not connected, or not found")
            exit()
        self.L3 = np.array([0. , 0.])
        self.R3 = np.array([0. , 0.])
        self.V = 0.
        self.angle = 0.
        self.Wrot = 0.

    def read(self):
        self.V = np.sqrt(self.L3[1]**2 + self.L3[0]**2)/100.
        self.angle = np.rad2deg(np.arctan2(-self.L3[0] , -self.L3[1]))
        self.Wrot = -self.R3[0]/250.
        if self.V <= 0.035:
            self.V = 0.
        if self.Wrot <= 0.035 and self.Wrot >= -0.035:
            self.Wrot = 0.
        return self.V, self.angle, self.Wrot
