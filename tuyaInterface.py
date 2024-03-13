import os
import json
import threading
import time
import tinytuya
from devicesData import DevicesData
from logger import logger

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
        logger.info (f"Send {command} to {id} : {self.tuyaDevices[id]}")
        ret = None
        if (command["switch"] == True):
            self.tuyaDevices[id].turn_on()
        elif (command["switch"] == False):
        logger.info (f"Command {command} to {id} returns {ret}")
        
    def poll(self, device ):
        '''
        Start MQTT threads, and then poll a device for status updates.

        Params:
            device:  An instance of Device dataclass
        '''

        logger.info('Connecting to %s', device['ip'])

        try:
            tuyaDevice = tinytuya.OutletDevice(device['id'], device['ip'], device['key'])
            tuyaDevice.set_version(device['version'])
            tuyaDevice.set_socketPersistent(True)
            self.tuyaDevices[device['id']] = tuyaDevice
            status = ""
        except Exception as e:
            logger.error("======== Exception 1 ========")
            logger.error(e)
            return

        while True:
            try:
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
                    logger.debug(f'STATUS for {device["id"]} :  {status}')
                except:
                    continue
            except Exception as e:
                logger.error("======== Exception 2 ========")
                logger.error(tuyaDevice)
                logger.error("------ Device -------")
                logger.error(device)
                logger.error("------ Status -------")
                logger.error(status)
                logger.error("------ DevicesData -------")
                logger.error(DevicesData.data)
                logger.error("===========================")
                        
            time.sleep(TIME_SLEEP)
