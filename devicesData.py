import os
import json
from datetime import datetime, timedelta

class DevicesDataClass:
    instance = None
    data = {}
    lastCommandDate = datetime.now()
    path = os.path.dirname(os.path.abspath(__file__))
    _observers = []

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(DevicesDataClass, cls).__new__(cls)
            cls.instance.load()
        return cls.instance
    
    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
    
    def setCommand(self, id, type, value):
        self.data[id]['commands'][type] = value
        self.notify_observers(id)

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
            for desc in data:
                self.data[desc["id"]] = {}
                self.data[desc["id"]]["desc"] = desc
                self.data[desc["id"]]["status"] = {}
                self.data[desc["id"]]["commands"] = {}
        
    def save(self):
        with open(self.path + '/config/snapshot.json', 'w') as jsonfile:
            json.dump(DevicesData.data, jsonfile, indent=2)
            
    def getIdFromName(self, name):
        for id, device in self.data.items():
            if device['desc']['name'] == name:
                return id
        return -1
    
    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self,id):
        for observer in self._observers:
            observer.onCommandReceived(id,self.data[id]['commands'])

# Exemple d'utilisation
DevicesData = DevicesDataClass()
