import time
import os
import pyads
import json
import os
# import paho.mqtt.client as mqtt  # Commenté pour l'exemple

def clear():
    os.system("cls")

# Initialisation de la connexion au PLC
def init_plc():
    plc = pyads.Connection('192.168.1.14.1.1', 851)
    plc.open()
    return plc

# Initialisation de la connexion MQTT (commentée pour l'exemple)
# def init_mqtt():
#     client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="data_publisher")
#     client.loop_start()
#     client.connect("192.168.1.10", 1883, 60)
#     return client

# Vérification si les données sont prêtes
def check_data_ready(plc):
    return plc.read_by_name('GVL.bDataReady', pyads.PLCTYPE_BOOL)

# Réinitialisation de l'indicateur de disponibilité des données
def reset_data_ready(plc):
    plc.write_by_name('GVL.bDataReady', False, pyads.PLCTYPE_BOOL)

# Vérification de l'état du tampon
def check_buffer_active(plc):
    return plc.read_by_name('GVL.bBufferActive', pyads.PLCTYPE_BOOL)

# Récupération des valeurs du tampon pour les deux capteurs
def get_buffer_values(plc, buffer_active):
    if buffer_active:
        x1_values = plc.read_by_name('GVL.rAnalogInputSensor1xValuesArrayA', pyads.PLCTYPE_ARR_REAL(1000))
        y1_values = plc.read_by_name('GVL.rAnalogInputSensor1yValuesArrayA', pyads.PLCTYPE_ARR_REAL(1000))
        x2_values = plc.read_by_name('GVL.rAnalogInputSensor2xValuesArrayA', pyads.PLCTYPE_ARR_REAL(1000))
        y2_values = plc.read_by_name('GVL.rAnalogInputSensor2yValuesArrayA', pyads.PLCTYPE_ARR_REAL(1000))
    else:
        x1_values = plc.read_by_name('GVL.rAnalogInputSensor1xValuesArrayB', pyads.PLCTYPE_ARR_REAL(1000))
        y1_values = plc.read_by_name('GVL.rAnalogInputSensor1yValuesArrayB', pyads.PLCTYPE_ARR_REAL(1000))
        x2_values = plc.read_by_name('GVL.rAnalogInputSensor2xValuesArrayB', pyads.PLCTYPE_ARR_REAL(1000))
        y2_values = plc.read_by_name('GVL.rAnalogInputSensor2yValuesArrayB', pyads.PLCTYPE_ARR_REAL(1000))
    return (x1_values, y1_values), (x2_values, y2_values)

# Fonction pour publier les données via MQTT (commentée pour l'exemple)
# def publish_data_mqtt(client, transmission_name, x_values, y_values):
#     # Préparation des données à envoyer
#     data_to_send = [transmission_name, x_values, y_values]
#     payload = json.dumps(data_to_send)  # Sérialisation en JSON
#     client.publish("data", payload=payload, qos=1)

plc = init_plc()
# client = init_mqtt()  # MQTT désactivé pour l'exemple

try:
    while True:
        while not check_data_ready(plc):
            time.sleep(0.1)  # Attente passive pour réduire la charge CPU

        buffer_active = check_buffer_active(plc)
        (x1_values, y1_values), (x2_values, y2_values) = get_buffer_values(plc, buffer_active)

        # Calculer et afficher la moyenne pour chaque capteur
        clear()
        print("Sensor 1 - Moyenne X:", sum(x1_values)/len(x1_values), "Y:", sum(y1_values)/len(y1_values))
        print("Sensor 2 - Moyenne X:", sum(x2_values)/len(x2_values), "Y:", sum(y2_values)/len(y2_values))

        reset_data_ready(plc)
        # time.sleep(9.9)  # Temps d'attente ajusté selon la nécessité

except KeyboardInterrupt:
    print("Arrêt manuel par l'utilisateur.")
finally:
    plc.close()
    # client.disconnect()  # MQTT désactivé pour l'exemple
