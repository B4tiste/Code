import time
import csv
import os
import pyads
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Initialisation de la connexion au PLC
def init_plc():
    plc = pyads.Connection('192.168.1.14.1.1', 851)
    plc.open()
    return plc

# Initialisation de la connexion MQTT
def init_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="data_publisher")
    client.loop_start()
    client.connect("localhost", 1883, 60)
    return client

# Vérification si les données sont prêtes
def check_data_ready(plc):
    return plc.read_by_name('GVL.bDataReady', pyads.PLCTYPE_BOOL)

# Réinitialisation de l'indicateur de disponibilité des données
def reset_data_ready(plc):
    plc.write_by_name('GVL.bDataReady', False, pyads.PLCTYPE_BOOL)

# Vérification de l'état du tampon
def check_buffer_active(plc):
    return plc.read_by_name('GVL.bBufferActive', pyads.PLCTYPE_BOOL)

# Récupération des valeurs du tampon
def get_buffer_values(plc, buffer_active):
    if buffer_active:
        x_values = plc.read_by_name('GVL.rAnalogInputSensor1xValuesArrayA')
        y_values = plc.read_by_name('GVL.rAnalogInputSensor1yValuesArrayA')
    else:
        x_values = plc.read_by_name('GVL.rAnalogInputSensor1xValuesArrayB')
        y_values = plc.read_by_name('GVL.rAnalogInputSensor1yValuesArrayB')
    return x_values, y_values

# Fonction pour publier les données via MQTT
def publish_data_mqtt(client, transmission_name, x_values, y_values):
    
    # Préparation des données à envoyer
    data_to_send = [transmission_name, x_values, y_values]
    payload = json.dumps(data_to_send)  # Sérialisation en JSON
    
    client.publish("data", payload=payload, qos=1)

plc = init_plc()
client = init_mqtt()

try:
    while True:
        while not check_data_ready(plc):
            time.sleep(0.01)  # Attente passive pour réduire la charge CPU

        buffer_active = check_buffer_active(plc)
        x_values, y_values = get_buffer_values(plc, buffer_active)

        date_folder = datetime.now().strftime("%Y-%m-%d")
        daily_folder_path = os.path.join('data', date_folder)
        os.makedirs(daily_folder_path, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(daily_folder_path, f"DATA_{timestamp}.csv")

        # Sauvegarde des données dans un fichier CSV
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["X", "Y"])
            for x_val, y_val in zip(x_values, y_values):
                writer.writerow([x_val, y_val])

        print(f"Les données ont été enregistrées dans {filename}")

        # Nom de la transmission (peut être basé sur le timestamp ou autre)
        transmission_name = f"Transmission_{timestamp}"

        # Publier les données via MQTT
        publish_data_mqtt(client, transmission_name, x_values, y_values)

        reset_data_ready(plc)

        time.sleep(0.99)

except KeyboardInterrupt:
    print("Arrêt manuel par l'utilisateur.")
finally:
    plc.close()
    client.disconnect()