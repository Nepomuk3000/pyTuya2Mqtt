import logging
from logging.handlers import RotatingFileHandler
import sys

def configurer_logger(level):
    # Créer un logger
    logger = logging.getLogger('tuya2mqtt')
    
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

    # Configurer un handler RotatingFileHandler pour enregistrer les logs dans un fichier
    file_handler = RotatingFileHandler('/tmp/tuya2mqtt.log', maxBytes=1e6, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Configurer un handler StreamHandler pour afficher les logs dans la console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def setLogLevel (level):
    logger.setLevel(level)

# Appeler la fonction configurer_logger() pour configurer le logger
logger = configurer_logger(logging.INFO)
