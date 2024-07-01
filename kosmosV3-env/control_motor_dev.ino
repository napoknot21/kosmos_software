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
#define step_mode 4 // 1 pour full_step, 2 pour 1/2 microstep, 16 pour 1/16 microstep etc
#define number_of_revolutions 10
#define max_speed 6000
#define max_acceleration 6000

// données reçues par communication Raspberry
#define pause_time 5000

// Create a new instance of the AccelStepper class:
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  // Set the maximum speed and acceleration:
  stepper.setMaxSpeed(max_speed);
  stepper.setAcceleration(max_acceleration);

  attachInterrupt(digitalPinToInterrupt(interrupt_pin), change_state, RISING);
}

void loop() {
  if (state) {
    // Set the target position:
    stepper.move(400*number_of_revolutions*step_mode);
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
