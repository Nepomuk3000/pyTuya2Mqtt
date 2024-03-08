import os
import json
from datetime import datetime, timedelta

class DevicesDataClass:
    instance = None
    data = {}
    lastCommandDate = datetime.now()
    path = os.path.dirname(os.path.abspath(__file__))

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(DevicesDataClass, cls).__new__(cls)
            cls.instance.load()
        return cls.instance
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
    
    def updateLastCommandDate(self):
        self.lastCommandDate = datetime.now()

    def commandReceivedRecently(self):
        # Calculer la différence entre les deux dates
        difference = abs(datetime.now() - self.lastCommandDate)
        
        # Vérifier si la différence est inférieure à 2 secondes
        if difference < timedelta(seconds=2):
            return True
        else:
            return False
        
    def load(self):
        with open(self.path + '/config/devices.json', 'r') as jsonfile:
            data = json.load(jsonfile)
            self.data = {}
            self.data[data[0]["id"]] = {}
            self.data[data[0]["id"]]["desc"] = data[0]
            self.data[data[0]["id"]]["status"] = {}
        
    def save(self):
        with open(self.path + '/config/snapshot.json', 'w') as jsonfile:
            json.dump(DevicesData.data, jsonfile, indent=2)
        
DevicesData = DevicesDataClass()
