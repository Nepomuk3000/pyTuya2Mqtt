import os
import json
import threading
import time
import tinytuya
import logging
from devicesData import DevicesData

logger = logging.getLogger(__name__)
TIME_SLEEP = 5


class tuyaInterface:
    tuyaDevices = {}
    
    def __init__(self):
        #tinytuya.set_debug()
        self.threads = []

    def start(self):
            
        DevicesData.add_observer(self)

        for key, device in DevicesData.data.items():
            threadPoll = threading.Thread(target=self.poll,args=(device["desc"],))
            self.threads.append(threadPoll)
            threadPoll.start()
            
    def onCommandReceived(self,id,command):
        if (command["switch"] == True):
            self.tuyaDevices[id].turn_on()
        elif (command["switch"] == False):
            self.tuyaDevices[id].turn_off()
        
    def poll(self, device ):
        '''
        Start MQTT threads, and then poll a device for status updates.

        Params:
            device:  An instance of Device dataclass
        '''

        logger.debug('Connecting to %s', device['ip'])

        tuyaDevice = tinytuya.OutletDevice(device['id'], device['ip'], device['key'])
        tuyaDevice.set_version(3.4)
        tuyaDevice.set_socketPersistent(True)
        self.tuyaDevices[device['id']] = tuyaDevice

        try:
            while True:
                status = tuyaDevice.status()
                for cle, valeur in status['dps'].items():
                    if cle in device['mapping']:
                        code=device['mapping'][cle]['code']
                        valueType=device['mapping'][cle]['type']
                        if valueType == "Integer":
                            scale=device['mapping'][cle]['values']['scale']
                            unit=device['mapping'][cle]['values']['unit']
                            value=valeur/(10 ** scale)
                        else:
                            value=valeur
                            unit=""
                        DevicesData[device["id"]]["status"][code] = value
                    else:
                        DevicesData[device["id"]]["status"][cle] = valeur
                try: 
                    logger.debug('STATUS:  %s', status)
                except:
                    continue
                        
                time.sleep(TIME_SLEEP)
        finally:
            print("---- Exception -----")
            print(DevicesData.data)
            print("--------------------")
