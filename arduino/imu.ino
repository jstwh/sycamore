#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

// create object (bno) of class Adafruit_BNO055
// 55 arbitrary unless multiple sensors used
Adafruit_BNO055 bno = Adafruit_BNO055(55);

void setup(void) {
  // put your setup code here, to run once:
  // start serial communication at baud rate 9600 bits/s
  Serial.begin(9600);

  // initialising sensor
  if(!bno.begin())
  { 
    // if false, (initialisation fails), print error message
    Serial.print("No BNO055 IMU sensor detected ... Check the wiring or 12C ADDR!");
    // enter infinite loop to prevent further running program
    while(1);
  }

  // wait 1s
  delay(1000);

  //bno.setExtCrystalUse(true);
}

void loop(void) {
  // put your main code here, to run repeatedly:
  // get a sensor event
  sensors_event_t event;
  bno.getEvent(&event);

  //show the data with 4 digits
  Serial.print("X: ");
  Serial.print(event.orientation.x, 4);
  Serial.print("\tY: ");
  Serial.print(event.orientation.y, 4);
  Serial.print("\tZ: ");
  Serial.print(event.orientation.z, 4);
  Serial.println("");

  delay(100);
}