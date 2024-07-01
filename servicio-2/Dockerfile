# Dockerfile con la imagen y pasos para dejar funcionando el servicio
# puede ser igual al del servicio-1 y servicio-3

# Dockerfile para servicio-2
FROM python:3.9-slim

WORKDIR /app

COPY service_2.py .

RUN pip install paho-mqtt influxdb-client

CMD ["python", "mqtt_to_influx.py"]