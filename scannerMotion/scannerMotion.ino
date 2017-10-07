/*
 * Operate two stepper motors using the adafruit V2 motor shield for Arduino to elevate the camera and turn the turntable based on serial commands
 * Using NEMA-17 stepper motors with 200 steps/rev
 */

#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect two steppers with 200 steps per revolution (1.8 degree)
Adafruit_StepperMotor *elevatorMotor = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *turnTableMotor = AFMS.getStepper(200, 2);

// you can change these to SINGLE, DOUBLE or INTERLEAVE or MICROSTEP

// wrappers for elevator motor
void down() { // turn the elevator stepper such that the load descends
  elevatorMotor->onestep(BACKWARD, SINGLE);
}
void up() {  // turn the elevator stepper such that the load ascends
  elevatorMotor->onestep(FORWARD, SINGLE);
}

// wrappers for the turn table motor
void counterClockWise() { // turn the turn table motor CCW
  turnTableMotor->onestep(FORWARD, SINGLE);
}
void clockWise() { // turn the turn table motor CW
  turnTableMotor->onestep(BACKWARD, SINGLE);
}

// Now we'll wrap the 3 steppers in an AccelStepper object
AccelStepper accelElevatorMotor(down, up);
AccelStepper accelTurnTableMotor(counterClockWise, clockWise);

// helper functions to dimensional analysis
int heightToSteps(int height) {
  // output how many steps to rotate given a height in mm we need to travel
  // this multiplier is a function of both the stepper motor and leadscrew
  // the stepper motor is 200 steps/rev and the leadscrew travels 8mm/rev
  int steps = height*(200/8);
  return steps;
}

int degToSteps(int deg) {
  // output how many steps to rotate given an angle to rotate through in deg
  // this multiplier is a function of the stepper motor
  // the stepper motor is 200 steps/rev
  int steps = deg*(200/360);
  return steps;
}

// move functions for elevator motor
void moveUp(int height) {
  int steps = heightToSteps(height);
  accelElevatorMotor.moveTo(steps);
  accelElevatorMotor.run();
}

void movedown(int height) {
  int steps = heightToSteps(height);
  accelElevatorMotor.moveTo(steps);
  accelElevatorMotor.run();
}

// move functions for turn table motor
void moveCCW(int deg) {
  int steps = degToSteps(deg);
  accelTurnTableMotor.moveTo(steps);
  accelTurnTableMotor.run(); 
}

void moveCW(int deg) {
  int steps = degToSteps(deg);
  accelTurnTableMotor.moveTo(accelTurnTableMotor.currentPosition() + 100);
  accelTurnTableMotor.run(); 
}

void setup(void) {
  AFMS.begin(); // start the motor shield

  // set speed and accel parameters for the stepper motors
  accelElevatorMotor.setMaxSpeed(200.0); // steps per second
  accelElevatorMotor.setAcceleration(400.0); // steps per second^2
    
  accelTurnTableMotor.setMaxSpeed(200.0); // steps per second
  accelTurnTableMotor.setAcceleration(400.0); // steps per second^2

  // initialize serial at 9600 baud to communicate with the controlling python script
  Serial.begin(9600);

  // attaches the servo on pin 9 to the servo object 
  theServo.attach(9);

  // reset the servo to the start position (INSTANTANEOUS MOVE)
  theServo.write(deg);
  
}

void loop(void) {

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

