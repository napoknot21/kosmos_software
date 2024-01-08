#!/bin/bash

#Effectuer une mise a jour la carte
sudo apt update

#Installation du dernier OS
sudo apt upgrade
sudo apt autoremove

#Telechargement de python 3
sudo apt install python3-pip

#Installation des packages necessaires 
cd kosmosV3-env
sudo pip install -r requirements.txt

#Recuperation du nom de la raspberry
nom_raspberry=$(whoami)
echo "$nom_raspberry"

#Recuperation du nom de la clef USB
USB_NAME=$(lsblk -o LABEL,MOUNTPOINT | grep "/media\|/mnt" | awk '{print $1}')
echo "$USB_NAME"

#Rendre le lancement.sh executable
cd kosmos_software
sudo chmod 755 lancement.py

#Activation de "Legacy camera" et "i2c"
cd ..
sudo raspi-config nonint do_i2c 0

#Ajout de la ligne de commande dans crontab qui permet le lancement au demarrage et création d'un dossier log
mkdir -p /home/$nom_raspberry/kosmos_software/logfile
(sudo crontab -l; echo "@reboot sudo python3 /home/$nom_raspberry/kosmos_software/lancement.py > /home/$nom_raspberry/kosmos_software/logfile/log.txt 2>&1";) | uniq - | sudo crontab
sudo crontab -l

exit 0
