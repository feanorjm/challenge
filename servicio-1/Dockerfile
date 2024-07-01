# Dockerfile con la imagen y pasos para dejar funcionando el servicio
# puede ser igual al del servicio-2 y servicio-3

# Dockerfile para servicio-1
FROM python:3.9-slim

WORKDIR /app

COPY service_1.py .

RUN pip install paho-mqtt

CMD ["python", "device_publisher.py"]
