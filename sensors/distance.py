import serial
import time
import threading


def measured_distance(ser):
    """Read and display distance measurements from the Arduino."""
    dists = ser.readline().decode("utf-8").strip()
    if dists:
        left, right = map(float, dists.split(","))
        return (left, right)
    else:
        return (None, None)


class DistanceReader(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.left = None
        self.right = None
        self.running = True

    def run(self):
        while self.running:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode("utf-8").strip()
                    self.left, self.right = map(float, line.split(","))
                except ValueError:
                    pass
                except serial.SerialException:
                    break

    def stop(self):
        self.running = False
        if self.ser.is_open:
            self.ser.close()


if __name__ == "__main__":
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
    time.sleep(1)  # Allow Arduino to reset
    measured_distance(ser)
