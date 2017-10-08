void setup() {
  // put your setup code here, to run once:

  
  // initialize serial at 9600 baud to communicate with the controlling python script
  Serial.begin(9600);
  Serial.println("-- STARTING --");
}

boolean which = true; //Flipping variable for either turntable or camera
boolean stringComplete;
String inputString = "";
int deg = 0;

void loop(void) {

  if (stringComplete) {

    deg = inputString.toInt();
//    if (which == true) { //if its stepper motor for camera
//      moveUp(deg);
//      }
//    if (which != true) { //if its stepper motor for turntable
////      moveCW(deg);
//      }
//    
    Serial.println(inputString);
    //Reassign string for next iteration
    which = !which;
    inputString = "";
    stringComplete = false;
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



