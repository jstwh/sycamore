import RPi.GPIO as GPIO
from hcsr04sensor import sensor

# set gpio pins
trig = 17
echo = 27

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
x = sensor.Measurement

# use default temp of 20 Celcius
distance = x.basic_distance(trig, echo)

print("The distance at (assumed) 20 Celsius is {} cm's".format(distance))

# cleanup gpio pins.
GPIO.cleanup((trig, echo))