import numpy as np
from flask_cors import CORS
from flask import Flask,request,make_response
from PIL import Image
import io
import os
import csv


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from kosmos_state import KState
from kosmos_config import *


class Server:
    
    app = Flask(__name__)

    def __init__(self,myMain):
        self.myMain=myMain
        CORS(self.app)
        
        self.app.add_url_rule("/state", view_func=self.state)
        self.app.add_url_rule("/start", view_func=self.start)
        self.app.add_url_rule("/stop", view_func=self.stop)
        self.app.add_url_rule("/shutdown", view_func=self.shutdown)
        self.app.add_url_rule("/getRecords", view_func=self.getRecords)
        self.app.add_url_rule("/changeConfig", view_func=self.changeConfig,methods=['POST'])
        self.app.add_url_rule("/getConfig", view_func=self.getConfig)
        self.app.add_url_rule("/changeCampagne", view_func=self.changeCampagne,methods=['POST'])
        self.app.add_url_rule("/getCampagne", view_func=self.getCampagne)
        self.app.add_url_rule("/frame", view_func=self.image)
        self.app.add_url_rule("/update-metadata", view_func=self.updateMetadata)

    def run(self) :
        logging.info("Server is running !")
        self.app.run(host="0.0.0.0",port=5000,debug=False)
            
    def state(self):
        return {
            "status" : "ok",
            "state" : str(self.myMain.state)
        }
        
    def start(self):
        if(self.myMain.state==KState.STANDBY):   
            self.myMain.record_event.set() 
            self.myMain.button_event.set()

            # get the video_path
            video_path = self.myMain.video_path

            return {
                "status" : "ok",
                "video_path": video_path
            }
        else :
            return {
                "status" : "error"
            }

    def stop(self):
        if(self.myMain.state==KState.WORKING):
            self.myMain.record_event.set()
            self.myMain.button_event.set()

            self.myMain.video_path = None
            return {
                "status" : "ok"
            }
        else :
            return {
                "status" : "error"
            }
    
    def shutdown(self):
        if(self.myMain.state==KState.STANDBY):
            self.myMain.stop_event.set()
            self.myMain.button_event.set()
            return {
                "status" : "ok"
            }
        else :
            return {
                "status" : "error"
            }
    
    
    def changeCampagne(self):
        if(self.myMain.state==KState.STANDBY):
            data = request.json
            for key in data:
                #self.myMain._conf.set_val(key,data[key])
                self.myMain._conf.config.set(CAMPAGNE_SECTION,key,data[key])
            self.myMain._conf.update_config()
            self.myMain.thread_camera.closeCam()
            
            # Désallocation des GPIOs avant reboot
            self.myMain._ledR.close()
            self.myMain._ledB.close()
            self.myMain.Button_Stop.close() 
            self.myMain.Button_Record.close()
            if self.myMain.PRESENCE_MOTEUR==1:
                self.myMain.motorThread.Relai_GPIO.close()
                self.myMain.motorThread.PWM_GPIO.close()
                self.myMain.motorThread.Button_motor.close()
            
            # Arrêt des Thread en cours
            if self.myMain.PRESENCE_MOTEUR==1:
                del self.myMain.motorThread
            del self.myMain.thread_camera
            
            # Réinitialisation
            self.myMain.init()
            self.myMain.button_event.set()
            return {
                "status" : "ok"
            }
        else:
            return {
                "status" : "error"
            }
        
    def getCampagne(self):
        response=dict()        
        response["data"] = dict(self.myMain._conf.config[CAMPAGNE_SECTION])
        response["status"]="ok"
        return response
    
    def changeConfig(self):
        if(self.myMain.state==KState.STANDBY):
            data = request.json
            for key in data:
                #self.myMain._conf.set_val(key,data[key])
                self.myMain._conf.config.set(CONFIG_SECTION,key,data[key])
            self.myMain._conf.update_config()
            self.myMain.thread_camera.closeCam()
            
            # Désallocation des GPIOs avant reboot
            self.myMain._ledR.close()
            self.myMain._ledB.close()
            self.myMain.Button_Stop.close() 
            self.myMain.Button_Record.close()
            if self.myMain.PRESENCE_MOTEUR==1:
                self.myMain.motorThread.Relai_GPIO.close()
                self.myMain.motorThread.PWM_GPIO.close()
                self.myMain.motorThread.Button_motor.close()
            
            # Arrêt des Thread en cours
            if self.myMain.PRESENCE_MOTEUR==1:
                del self.myMain.motorThread
            del self.myMain.thread_camera
            
            # Réinitialisation
            self.myMain.init()
            self.myMain.button_event.set()
            return {
                "status" : "ok"
            }
        else:
            return {
                "status" : "error"
            }
        
    def getConfig(self):
        response=dict()        
        response["data"] = dict(self.myMain._conf.config[CONFIG_SECTION])
        response["status"]="ok"
        return response
    

    def getRecords(self):
        response=dict()
        try:
            outputList=[]
            strr="ls -l -R " + self.myMain._conf.CAMPAGNE_PATH 
            stream =os.popen(strr)       
            streamOutput = stream.read()
            strRef=streamOutput.split('\n/')
            strRef2=strRef[1].split('\n-')

            for i in range(1,len(strRef)):
                strRef2=strRef[i].split('\n-')
                for j in range(1,len(strRef2)):
                    d=dict()
                    data=strRef2[j].split()
                    d["size"]="{:.4f}".format(int(data[4])/(1024**2))
                    d["month"]=data[5]
                    d["day"]=data[6]
                    d["time"]=data[7]
                    d["fileName"]=data[8]
                    outputList.append(d)
        except:
           outputList=[] 
        response["data"]=outputList
        response["status"]="ok"
        return response


    def image(self):
        camera=self.myMain.thread_camera._camera
        buf=io.BytesIO()
        camera.options["quality"]=10 # compression pour fluidifier
        camera.capture_file(buf,format='jpeg')
        response=make_response(buf.getvalue())
        response.headers['Content-Type']='image/jpg'
        return response    

        
    def updateMetadata(self):
        if (self.myMain.state == KState.STOPPING or self.myMain.state == KState.STANDBY):
            data = request.json
        
            try:
                # Changer de répertoire pour le chemin vidéo spécifié
                os.chdir(data['video_path'])

                # Créer le fichier metadata.csv et y écrire les en-têtes et les données
                with open('metadata.csv', mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')

                    # En-têtes du fichier CSV
                    writer.writerow([
                        "Code Station", "Heure", "Minute", "Seconde",
                        "Site", "Latitude", "Longitude",
                        "Profondeur", "Température", "Salinité",
                        "Lune", "Marée", "Coefficient",
                        "Ciel", "Vent", "Direction", "Pression Atm", "Temp. Air",
                        "État de la Mer", "Houle",
                        "Exploitabilité", "Habitat", "Faune", "Visibilité"
                    ])

                    # Récupération des données pour chaque section
                    codeStation = data.get('codeStation', '')
                    heure = data['heureDict'].get('heure', '')
                    minute = data['heureDict'].get('minute', '')
                    seconde = data['heureDict'].get('seconde', '')
                    site = data['gpsDict'].get('site', '')
                    latitude = data['gpsDict'].get('latitude', '')
                    longitude = data['gpsDict'].get('longitude', '')
                    profondeur = data['ctdDict'].get('profondeur', '')
                    temperature = data['ctdDict'].get('temperature', '')
                    salinite = data['ctdDict'].get('salinite', '')
                    lune = data['astroDict'].get('lune', '')
                    maree = data['astroDict'].get('maree', '')
                    coefficient = data['astroDict'].get('coefficient', '')
                    ciel = data['meteoAirDict'].get('ciel', '')
                    vent = data['meteoAirDict'].get('vent', '')
                    direction = data['meteoAirDict'].get('direction', '')
                    atmPress = data['meteoAirDict'].get('atmPress', '')
                    tempAir = data['meteoAirDict'].get('tempAir', '')
                    etatMer = data['meteoMerDict'].get('etatMer', '')
                    houle = data['meteoMerDict'].get('houle', '')
                    exploitabilite = data['analyseDict'].get('exploitabilite', '')
                    habitat = data['analyseDict'].get('habitat', '')
                    faune = data['analyseDict'].get('faune', '')
                    visibilite = data['analyseDict'].get('visibilite', '')

                    # Écrire les données dans le fichier CSV
                    writer.writerow([
                        codeStation, heure, minute, seconde,
                        site, latitude, longitude,
                        profondeur, temperature, salinite,
                        lune, maree, coefficient,
                        ciel, vent, direction, atmPress, tempAir,
                        etatMer, houle,
                        exploitabilite, habitat, faune, visibilite
                    ])

                return {
                    "status": "ok"
                }

            except Exception as e:
                logging.error(f"Erreur lors de la création du fichier metadata.csv : {e}")
                return {
                    "status": "error"
                }

        else:
            return {
                "status": "error"
            }
