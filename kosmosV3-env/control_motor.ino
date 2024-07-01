#include "AccelStepper.h"
#include <Wire.h>
#define SLAVE_ADDRESS 0x04       // I2C address for Arduino

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 4
#define stepPin 5

// paramètres d'interruption
#define interrupt_pin 2
#define motorInterfaceType 1
volatile unsigned long button_time = 0;
volatile unsigned long last_button_time = 0;
int debounce = 2000;

//état de l'interrupteur ILS
bool state = false;

// structures pour les infos i2c
int Data = 1;
int Data_indent = 0;
int i2cData[5] = {};

// paramètres rotation moteur transmissibles par la Raspberry
int number_of_revolutions = 10,
    max_speed = 150,
    max_acceleration = 150,
    pause_time = 5,
    step_mode = 4; // 1 pour full_step, 2 pour 1/2 microstep, 4 pour 1/4 microstep, 16 pour 1/16 microstep etc


// Création d'une instance de classe AccelStepper:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  // Set the maximum speed and acceleration:
  stepper.setMaxSpeed(max_speed*step_mode*10);
  stepper.setAcceleration(max_acceleration*step_mode*10);

  // définition de l'interruption liée à l'ILS pour déclencher le fonctionnement moteur indépendant
  attachInterrupt(digitalPinToInterrupt(interrupt_pin), change_state, RISING);

  // setup de la communication i2c avec la Raspberry
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveData);
  Wire.onRequest(sendData);

  //setup communication série avec l'ordinateur
  Serial.begin(9600);
}

void loop() {
  if (state) {
    // Set the target position:
    stepper.move(400*number_of_revolutions*step_mode);

    // Run to target position with set speed and acceleration/deceleration:
    stepper.runToPosition();

    // Attente entre 2 rotations
    delay(pause_time*1000);
  }
  for (int j = 0; j<=4; j++){
    Serial.print(i2cData[j]);
    Serial.print(" ; ");
    }
  Serial.println("");
  delay(1000);
}

// fonction appelée par l’interruption externe n°0
void change_state()
{
  button_time = millis();
  if (button_time > last_button_time + debounce) {
    state = !state;  // inverse l’état de la variable
    last_button_time = button_time;
  }
}

// fonction appelée à la réception d'un octet i2c 
void receiveData(int byteCount) {
  while (Wire.available()) {
    Data = Wire.read();
    if (!Data) {Data_indent = 0;}
    else{
      i2cData[Data_indent] = Data;
      ++Data_indent;
    }
    if (Data_indent == 6) {
      state = i2cData[0];
      number_of_revolutions = i2cData[1];
      stepper.setMaxSpeed(i2cData[2]*step_mode*10);
      stepper.setAcceleration(i2cData[3]*step_mode*10);
      pause_time = i2cData[4];
      step_mode = i2cData[5];
    }
  }
}

// fonction appelée par requête de la Raspberry
void sendData() {
  Wire.write(1);
}
