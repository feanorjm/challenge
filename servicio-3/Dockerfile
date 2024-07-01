# Dockerfile con la imagen y pasos para dejar funcionando el servicio
# puede ser igual al del servicio-1 y servicio-2

# Dockerfile para servicio-3
FROM python:3.9-slim

WORKDIR /app

COPY service_3.py .

RUN pip install flask influxdb-client mysql-connector-python

CMD ["python", "service_3.py"]