#include <LiquidCrystal.h>

LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

const int trigger_pin_left = 3;
const int echo_pin_left = 2;
const int trigger_pin_right = 5;
const int echo_pin_right = 4;

float speed_of_sound = 343.2611; //Meters per second at 20C (ADJUST FOR DIFF TEMPS!)
float conversion_factor = .0001;
unsigned int ping_time = 0;

bool ip_displayed = false;
String ip_address = "";

void setup() {
  pinMode(trigger_pin_left, OUTPUT);
  pinMode(echo_pin_left, INPUT);
  pinMode(trigger_pin_right, OUTPUT);
  pinMode(echo_pin_right, INPUT);
  Serial.begin(9600);
  lcd.begin(16, 2);
  lcd.print("Waiting for IP");
}

float distance(int triggerPin, int echoPin) {
  /* distance returns a float value in centimeters */
  float dist = 0.0;

  digitalWrite(triggerPin, LOW);
  delayMicroseconds(5);
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(12);
  digitalWrite(triggerPin, LOW);
  ping_time = pulseIn(echoPin, HIGH, 18000);

  if (ping_time == 0) {
    return -1; // Return -1 if no valid echo received
  }

  dist = speed_of_sound * conversion_factor * ping_time / 2;
  return dist;
}

void loop() {
  // Handle IP Address Display
  if (Serial.available() > 0 && !ip_displayed) {
    ip_address = Serial.readStringUntil('\n');
    lcd.clear();
    lcd.print(ip_address);
    ip_displayed = true;
  }

  // Handle Distance Measurement
  if (ip_displayed) {
    float answer_left = distance(trigger_pin_left, echo_pin_left);
    float answer_right = distance(trigger_pin_right, echo_pin_right);

    Serial.println(String(answer_left) + "," + String(answer_right));

    delay(200);
  }
}