
#include <Wire.h>
#define SLAVE_ADDRESS 0x04       // I2C address for Arduino

int Data = 1;
int Data_indent = 0;
int i2cData[5] = {};                 // the I2C data received
int step_mode = 1;
int number_of_revolutions = 1;
int max_speed = 0;
int max_acceleration = 0;
int pause_time = 5000;

void setup(){
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
}
void loop() {
  for (int j = 0; j<=4; j++){
    Serial.print(i2cData[j]);
    Serial.print(" ; ");
    }
  Serial.println("");
  delay(5000);
}
// Handle reception of incoming I2C data
void receiveData(int byteCount) {
  while (Wire.available()) {
    Data = Wire.read();
    if (!Data) {Data_indent = 0;}
    else{
      i2cData[Data_indent] = Data;
      ++Data_indent;
    }
  }
}

// Handle request to send I2C data
void sendData() {
  Wire.write(1);
}
