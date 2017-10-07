// Camera based depth perception for doors algorithm development
// Trey Fortmuller

/*
 * turn a servo through a 60 sweep taking pictures with the webcam at incremental locations 
 * throughout the sweep to create a dataset of images with known extrinsics for openMVG structure from motion
 * 
 * servo signal lead: pin 9
 * servo power lead: 5V output pin
 * sevo ground lead: GND pin
 * 
 * OPERATIONAL RANGE OF THE SERVO IS (20deg to 170deg) INCLUSIVE
 * 
 */

#include <Servo.h> 

Servo theServo;  // create servo object to control a servo 

// CONSTANTS and VARIABLES
int servoPin = 9;  // the pin the servo is connected to
int center = 90;  // the position of the servo in degrees where the servo horn is squared (either parallel or perpendicular) to the servo body
int deg = center;  // the angle to set the servo to
int currentPos = center;  // the current position of the servo
int servoStep = 0;  // index for the for loops defining the speed of the servo
int turningSpeed = 20;  // update frequency in microseconds (a greater value is a slower turning rate)
String inputString = "";         // a string to hold incoming serial data
boolean stringComplete = false;  // when the string is complete we have a voltage command

void setup() 
{ 
  // initialize serial at 9600 baud to communicate with the controlling python script
  Serial.begin(9600);

  // attaches the servo on pin 9 to the servo object 
  theServo.attach(9);

  // reset the servo to the start position (INSTANTANEOUS MOVE)
  theServo.write(deg);

} 

 
void loop() {

  if (stringComplete) {

    deg = inputString.toInt();

    if (deg > 170 || deg < 20) {
      Serial.println("invalid value for this servo! Operational range is [20. 170] for some reason.");
      Serial.print("writing value: ");

    }
    else {
      if (deg >= currentPos) {
        Serial.print("writing value: ");
        Serial.println(deg);
  
        for (servoStep = currentPos + 1; servoStep <= deg; servoStep += 1) {
            theServo.write(servoStep);  // sets the servo position according to the deg value received from serial
            delay(15);
            Serial.println("moving up");
        }
        currentPos = deg;  
      }
      else {
        Serial.print("writing value: ");
        Serial.println(deg);
  
        for (servoStep = currentPos - 1; servoStep >= deg; servoStep -= 1) {
            theServo.write(servoStep);  // sets the servo position according to the deg value received from serial
            delay(15);
            Serial.println("moving down");
        }
        currentPos = deg;  
      }
    }

    inputString = "";
    stringComplete = false;
    Serial.print("Current value: ");
    Serial.println(currentPos);
  }

  // send data only when you receive data:
  if (Serial.available() > 0) {
    
    // read the incoming byte:
    char inChar = (char)Serial.read();

    // add it to the inputString
    inputString += inChar;
    
    // if the incoming character is a newline, set a flag, we have a voltage (pwm) command
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
