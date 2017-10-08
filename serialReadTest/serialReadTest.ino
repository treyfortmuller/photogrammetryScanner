void setup() {
  // put your setup code here, to run once:

  
  // initialize serial at 9600 baud to communicate with the controlling python script
  Serial.begin(9600);
  Serial.print("here");
}

void loop() {
  // put your main code here, to run repeatedly:
    // send data only when you receive data:
  if (Serial.available() > 0) {
    
    // read the incoming byte:
    char inChar = (char)Serial.read();
    Serial.print(inChar);
    Serial.write(inChar);
  }
}
