#include "AccelStepper.h"

// Define stepper motor connections and motor interface type. Motor interface type must be set to 1 when using a driver:
#define dirPin 4
#define stepPin 5

// paramètres d'interruption
#define interrupt_pin 2
#define motorInterfaceType 1
volatile unsigned long button_time = 0;
volatile unsigned long last_button_time = 0;
int debounce = 2000;

bool state = false;

// paramètres rotation moteur
#define one_revolution 12800

// données reçues par communication Raspberry
#define pause_time 5000

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  // Set the maximum speed and acceleration:
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(1000);

  attachInterrupt(digitalPinToInterrupt(interrupt_pin), change_state, RISING);
}

void loop() {
  if (state) {
    // Set the target position:
    stepper.move(one_revolution);
    // Run to target position with set speed and acceleration/deceleration:
    stepper.runToPosition();

    delay(pause_time);
  }
}

void change_state()  // la fonction appelée par l’interruption externe n°0
{
  button_time = millis();
  if (button_time > last_button_time + debounce) {
    state = !state;  // inverse l’état de la variable
    last_button_time = button_time;
  }
}
