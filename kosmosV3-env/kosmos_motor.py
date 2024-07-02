#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Controle du moteur via communication i2c avec Arduino Nano
Le code ci-dessous envoie une liste de paramètres à l'Arduino qui permet de modifier le comportement de la rotation moteur
"""
import logging
from gpiozero import Button, DigitalOutputDevice, PWMOutputDevice
from threading import Thread
from threading import Event
import time

try:
    import smbus
except:
    print ('Try sudo apt install python3-smbus2') #D. Hanon ajout de () pour être compatible python_3

from kosmos_config import *

class kosmosMotor(Thread):

    def __init__(self, aConf: KosmosConfig):
        
        Thread.__init__(self)

        try:
            self._bus = smbus.SMBus(bus)
        except:
            print("Bus %d is not available.") % bus
            print("Available busses are listed as /dev/i2c*")
            self._bus = None
        
        # Evénement pour commander l'arrêt du Thread
        self._pause_event = Event()
        self._continue_event = Event()
        self._t_stop = False 

        self._address = 0x04
        self._state = 0
        
        # Paramètres Moteur
        self.pause_time = aConf.get_val_int("13_MOTOR_pause_time") # en s
        self.motor_vitesse = aConf.get_val_int("11_motor_vitesse") # minimum : 1 ; maximum : 250
        self.motor_accel = aConf.get_val_int("12_motor_acceleration") # minimum : 1 ; maximum : 250
        self.motor_revolutions = aConf.get_val_int("10_motor_revolutions") # 10 revolutions : 60°
        self.step_mode = aConf.get_val_int("14_motor_step_mode") # 1 pour full_step, 2 pour 1/2 microstep, 4 pour 1/4 microstep, 16 pour 1/16 microstep etc
        self.i2c_period = aConf.get_val_int("15_motor_i2c_communication_period") # en s

    def power_off(self):
        """Commande l'arrêt de la rotation moteur (fonction appelée par la main en cas de shutdown)"""
        self._state = 0
        self.send_data()

    def send_data(self):
        i2c_Data = [self._state + 1, self.motor_revolutions, self.motor_vitesse, self.motor_accel, self.pause_time, self.step_mode]
        bus.write_i2c_block_data(self._address, 0x00, i2cData)
        if bus.read_byte(address) :
            logging.info('paramètres moteurs reçus par l'Arduino')
        else :
            logging.info('Erreur transmission Arduino i2c')
    
    def autoArm(self): 
        '''activation de la rotation moteur 1 fois pour témoigner de son fonctionnement à l'allumage'''
        time.sleep(2)
        
        self._state = 1
        self.send_data()

        time.sleep(1)
        
        self._state = 0
        self.send_data()
        
        logging.info('Moteur prêt !')
        
    def arret_complet(self):
        self.PWM_GPIO.off()
    
    def run(self):
        logging.info('Debut du thread moteur.')
        while not self._t_stop:
            if not self._pause_event.isSet():
                while not self._pause_event.isSet():
                    self._state = 1
                    self.send_data()
                    time.sleep(self.i2c_period)
            else:
                self._state = 0
                self.send_data()
                self._continue_event.wait()  
        # End While        
        self.arret_complet() #stop relai
        logging.info("Thread moteur terminé")
   
    def stop_thread(self):
        """positionne l'évènement qui va provoquer l'arrêt du thread"""
        self._t_stop = True
        self._continue_event.set()
        self._pause_event.set()
  
    def pause(self):
        """suspend le thread pour pouvoir le redémarrer."""
        self._continue_event.clear()
        self._pause_event.set()

    def restart(self):
        """Relance le thread"""
        if self.is_alive():
            self._pause_event.clear()
            self._continue_event.set()
        else:
            self.start()
          
