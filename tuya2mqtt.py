from tuyaInterface import tuyaInterface
from mqttInterface import mqttInterface
from logger import *
import argparse

if __name__ == "__main__":
    # Configurer l'analyseur d'arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Configurer le niveau de log au lancement.')
    parser.add_argument('-l', '--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    args = parser.parse_args()

    # Convertir le niveau de log en niveau de gravité
    setLogLevel(getattr(logging, args.log_level))
    
    tuya = tuyaInterface()

    tuya.start()

    mqtt = mqttInterface()

    #tuya.join()

