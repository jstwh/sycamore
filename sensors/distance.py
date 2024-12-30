import serial
import time


def measured_distance(ser):
    """Read and display distance measurements from the Arduino."""
    dists = ser.readline().decode("utf-8").strip()
    if dists:
        left, right = map(float, dists.split(","))
        return left, right
    else:
        return None, None


if __name__ == "__main__":
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
    time.sleep(1)  # Allow Arduino to reset
    measured_distance(ser)
