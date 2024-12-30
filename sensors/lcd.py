import socket
import serial
import time


def get_ip():
    """Fetch the RaspberryPI's IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr


def send_ip_to_arduino(ip_addr, ser):
    """Send the IP address to the Arduino over serial."""
    ser.write(f"{ip_addr}\n".encode("utf-8"))
    time.sleep(1)  # Give Arduino time to display IP


if __name__ == "__main__":
    ip = get_ip()
    ser = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
    time.sleep(1)  # Allow Arduino to reset
    send_ip_to_arduino(ip, ser)
