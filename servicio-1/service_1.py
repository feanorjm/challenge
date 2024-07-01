import paho.mqtt.client as mqtt
import json
from datetime import datetime
import random
import time


# Configuración de MQTT
BROKER = "mosquitto"
PORT = 1883
TOPIC = "challenge/dispositivo/rx"


def generate_message():
    message = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "value": round(random.uniform(0, 1000), 2),
        "version": random.randint(1, 2)
    }
    return json.dumps(message)


def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker con código de resultado {rc}")


client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)

client.loop_start()

try:
    while True:
        message = generate_message()
        a = client.publish(TOPIC, message)
        print(f"Mensaje publicado: {message}")
        time.sleep(10)  # Espera de 1 minuto
except KeyboardInterrupt:
    print("Interrumpido por el usuario")

client.loop_stop()
client.disconnect()
