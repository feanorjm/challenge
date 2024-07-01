# Servicio-1

Este servicio debe simular un dispositivo electrónico que envía mensajes a una cola MQTT.
Al comenzar a funcionar, cada 1 minuto, debe publicar el siguiente mensaje en el tópico `challenge/dispositivo/rx` del servicio mqtt(mosquitto).

```json
{
    "time": datetime,
    "value": random(0, 1000),
    "version": random(1, 2) 
}
```
Donde **datetime** es la fecha y hora del momento de publicación, **value** es un número flotante aleatorio entre 0 y 100. **version** es un número entero aleatorio que solo puede ser 1 o 2 y representa la versión del dispositivo.

Ejemplo

```json
{
    "time": "2022-01-01 10:00:00",
    "value": 566.45,
    "version": 1
}
```