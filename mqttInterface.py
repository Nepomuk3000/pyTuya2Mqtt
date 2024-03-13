import paho.mqtt.client as mqtt
from paho.mqtt import publish

import binascii
from struct import *
import json
import threading
import time
from datetime import datetime
import os
from devicesData import DevicesData
from logger import logger

class mqttInterface:
    
    def __init__ (self):
        
        # Paramètres du broker MQTT
        broker_address = "192.168.1.107"
        broker_port = 1883
        self.topic = "tuya/+/cmd"
        # Ouvrir le fichier JSON en mode lecture
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + '/config/credentials.json', 'r') as fichier:
            # Charger les données JSON à partir du fichier
            data = json.load(fichier)

            # Accéder aux valeurs des champs "user" et "passwd"
            username = data["user"]
            password = data["password"]

        # Création d'un client MQTT
        self.client = mqtt.Client()

        # Configuration des callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connexion au broker MQTT
        self.client.username_pw_set(username, password)
        self.client.connect(broker_address, broker_port, 60)

        self.thread = threading.Thread(target=self.sendMqttSatus)
        
        # Boucle principale du client
        self.client.loop_forever()
        
        for id, device in DevicesData.data.items():
            name = device['desc']['name']
            mac = device['desc']['mac']
            model = device['desc']['model']
            version = device['desc']['version']
        
            data = {
                'name': name,
                'unique_id': id,
                'availability_topic': f'home/{id}/online',
                'state_topic': f'home/{id}/fan/state',  # fan ON/OFF
                'command_topic': f'home/{id}/fan/command',
                'percentage_state_topic': f'home/{id}/fan/speed/state',
                'percentage_command_topic': f'home/{id}/fan/speed/command',
                'device': {
                    'identifiers': [{id}, mac],
                    'name': name,
                    'manufacturer': 'TBD',
                    'model': model,
                    'sw_version': f'tinytuya {version}',
                }
            }

            # self.client.publish("homeassistant/fan/id/config", json.dumps(data))

    # Callback appelée lorsqu'une connexion au broker est établie
    def on_connect(self, client, userdata, flags, rc):
        #log.info(f"Connecté au broker avec le code de retour {rc}")
        self.client.subscribe(self.topic)
        if not self.thread.is_alive():
            self.thread.start()
        
    def sendMqttSatus(self):
        while True:
            dateStr=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for id, device in DevicesData.data.items():
                device = DevicesData[id]
                device['date'] = dateStr
                message = json.dumps(device,indent=2)
                topic = f"tuya/{device['desc']['name']}/stat"
                self.client.publish(topic, message)
                DevicesData.save()
            time.sleep(5)

    # Callback appelée lorsqu'un message est reçu du broker
    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        # TODO rendre ça générique
        if (topic == "tuya/Compteur Garage/cmd"):
            if payload == "on" or payload == "off":
                id = DevicesData.getIdFromName("Compteur Garage")
                DevicesData.setCommand(id,"switch",payload=="on")
            else:
                logger.error (f"Err : Unable to process topic {topic}")
        else:
            logger.error (f"Err : Payload {payload} is not supported for topic {topic}")
