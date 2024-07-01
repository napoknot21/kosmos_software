/* 
 * Arduino code to send and receive I2C data
 */
#include <Wire.h>
#define SLAVE_ADDRESS 0x04       // I2C address for Arduino
int i2cData = 0;                 // the I2C data received
void setup(){
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);
  Serial.begin(9600);
}
void loop() {
  // Everything happens in the interrupts
}
// Handle reception of incoming I2C data
void receiveData(int byteCount) {
  while (Wire.available()) {
    i2cData = Wire.read();
    Serial.println(i2cData);
  }
}

// Handle request to send I2C data
void sendData() { 
  Wire.write(i2cData);
}
