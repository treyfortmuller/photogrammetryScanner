/* Greg the 3D Scanner -- Trey Fortmuller, Nathan Le, Suneel Belkhale
 * Operate two stepper motors using the adafruit V2 motor shield for Arduino to elevate the camera and turn the turntable based on serial commands
 * Using NEMA-17 stepper motors with 200 steps/rev
 */

#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect two steppers with 200 steps per revolution (1.8 degree)
Adafruit_StepperMotor *elevatorMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *turnTableMotor = AFMS.getStepper(200, 1);

boolean which = false; // flipping variable for either turntable or camera, true is elevator, false is turntable
boolean stringComplete;
String inputString = "";
int output = 0;

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

// Now we'll wrap both steppers in an AccelStepper object
AccelStepper accelElevatorMotor(down, up);
AccelStepper accelTurnTableMotor(counterClockWise, clockWise);

// helper functions for dimensional analysis
int heightToSteps(int height) {
  // output how many steps to rotate given a height in mm we need to travel
  // this multiplier is a function of both the stepper motor and leadscrew
  // the stepper motor is 200 steps/rev and the leadscrew travels 8mm/rev
  int steps = height*(200.0/8.0);
  return steps;
}

int degToSteps(int deg) {
  // output how many steps to rotate given an angle to rotate through in deg
  // this multiplier is a function of the stepper motor
  // the stepper motor is 200 steps/rev
  int steps = deg*(200.0/360.0);
  return steps;
}

// move functions for elevator motor
void moveElevator(int height) {
  int steps = heightToSteps(height);
  accelElevatorMotor.moveTo(-steps);
}

// move functions for turn table motor
void moveTurnTable(int deg) {
  int steps = degToSteps(deg);
  accelTurnTableMotor.moveTo(steps);
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
  
}
void loop(void) {

  // continually "run" each motor, steps are only commanded if the current setpoint has not been achieved.
  accelTurnTableMotor.run(); 
  accelElevatorMotor.run();

  if (stringComplete) {

    output = inputString.toInt();
    if (which == true) { // if its stepper motor for elevator
      moveElevator(output);
    }
    if (which != true) { // if its stepper motor for turntable
      moveTurnTable(output);
    }
    
    //Reassign string for next iteration
    which = !which;
    inputString = "";
    stringComplete = false;
  }

  // recieve incoming messages from the serial port
  if (Serial.available() > 0) {
    
    // read the incoming byte:
    char inChar = (char)Serial.read();

    // add it to the inputString
    inputString += inChar;
    
    // if the incoming character is a newline, set a flag, we have a new command completed
    if (inChar == '\n') {
      stringComplete = true;
      Serial.println(inputString)
    }
  }
}

