import serial
import threading


class DistanceReader(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.left = None
        self.right = None
        self.running = True
        self.ip_displayed = False

    def run(self):
        while self.running:
            if self.ser.in_waiting > 0:
                try:
                    # if self.ip_displayed == False:
                    #     self.send_ip_to_arduino(get_ip(), self.ser)
                    #     print("ip displayed")
                    #     self.ip_displayed = True
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
