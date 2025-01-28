#include <Servo.h>
Servo test1;
Servo test2;

int pos_X = 90;
int pos_Y = 90;

const int SW_pin = 8;
const int X_pin = 0;
const int Y_pin = 1;

void setup(){ 
   pinMode(SW_pin, INPUT);
   digitalWrite(SW_pin, HIGH);
   Serial.begin(9600);

   test1.attach(9);
   test2.attach(10);
}

String receivedData = ""; 

void loop() {
  while (Serial.available()) {
        char receivedChar = Serial.read();  // Read one character at a time
        
        if (receivedChar == '\n') {  // End of message (newline character)
            pos_Y = receivedData.toDouble() + 90;  // Convert the remaining string to y_pos
            // Serial.print("Received x: ");
            // Serial.print(x_pos);
            // Serial.print(", y: ");
            // Serial.println(y_pos);  // Print both x_pos and y_pos
            receivedData = "";  // Clear the buffer for the next message
            break;
        } else if (receivedChar == ' ') {  // Space indicates the end of x_pos
            pos_X = receivedData.toDouble() + 90;  // Convert receivedData to x_pos
            receivedData = "";  // Clear the buffer to start parsing y_pos
        } else {
            receivedData += receivedChar;  // Append character to buffer
        }
    }

  static int last_X = 90, last_Y = 90;
  if (pos_X != last_X || pos_Y != last_Y) {
      test1.write(pos_X);
      test2.write(pos_Y);
      last_X = pos_X;
      last_Y = pos_Y;
  }

  delay(15);
}