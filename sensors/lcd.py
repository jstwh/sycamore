import socket
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


def display_ip(ser):
    ip = get_ip()
    time.sleep(1)  # TODO find better way to do this
    send_ip_to_arduino(ip, ser)
