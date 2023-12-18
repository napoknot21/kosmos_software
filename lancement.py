#!/usr/bin/env python3 -- coding: utf-8 --

import configparser
import time
from datetime import datetime
import os




def executer_kosmos_main():
			
	os.system("cd /home/kosmosimt/kosmos_software/kosmosV3-env && sudo python kosmos_main.py")
		
	
def mode_heures_precises(heures_precises, SETT_RECORD_TIME):
	
	
	while True:
		heure_actuelle = time.strftime("%H:%M")

		if heure_actuelle in heures_precises:
			print(f"Demarrage de l'enregistrement à {heure_actuelle}")
			executer_kosmos_main()
			
time.sleep(60)
config = configparser.ConfigParser()
config.read('/media/kosmosimt/KOSMOS_CLE/kosmos_config.ini')

SETT_MODE = int(config.get('KOSMOS', 'SETT_MODE'))
SETT_RECORD_TIME = int(config.get('KOSMOS', 'SETT_RECORD_TIME'))
heures_precises = config.get('KOSMOS','SETT_HEURES_PRECISES')


	

if SETT_MODE == 0:
	mode_heures_precises(heures_precises, SETT_RECORD_TIME)
else:
	executer_kosmos_main()
	
	
	
