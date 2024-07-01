import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

# Configuración de MQTT
BROKER = "mosquitto"
PORT = 1883
TOPIC = "challenge/dispositivo/rx"

# Configuración de InfluxDB
INFLUXDB_URL = "http://localhost:32773/"
INFLUXDB_TOKEN = "GFXIISVUqdA3N8CzcjN_EtZ50lAgeMO_VxJiYKWL1o2AC2DwQO33iSWix8Iy14Un1rtY2ZAgFhb62JZ7TqTbDA=="
INFLUXDB_ORG = "tecnoandina"
BUCKET = "system"
MEASUREMENT = "dispositivos"

# Inicialización del cliente InfluxDB
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
print(client.url)
write_api = client.write_api(write_options=SYNCHRONOUS)


# Función cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(msg)
    try:
        message = json.loads(msg.payload.decode())
        print(message)
        point = Point(MEASUREMENT) \
            .field("time", message["time"]) \
            .field("value", message["value"]) \
            .tag("version", message["version"])
        write_api.write(bucket=BUCKET, org=INFLUXDB_ORG, record=point)
        print(f"Mensaje insertado en InfluxDB: {message}")
    except Exception as e:
        print(f"Error al insertar el mensaje en InfluxDB: {e}")


# Función cuando se conecta al broker
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Conectado al broker con código de resultado {rc}")
    client.subscribe(TOPIC)


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect(BROKER, PORT, 60)

mqtt_client.loop_forever()
