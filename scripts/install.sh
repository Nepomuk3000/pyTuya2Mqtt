serviceName="tuya2mqtt"
pip install tinytuya

# Copier le ficheir de service a l'emplacement approprié
cp ${serviceName}.service /etc/systemd/system/

# Activer le service
systemctl enable ${serviceName}.service

# Lancer le service
systemctl start ${serviceName}.service

