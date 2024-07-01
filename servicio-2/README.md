# Servicio-2

Este servicio debe escuchar el tópico `challenge/dispositivo/rx` del servicio mqtt(mosquitto).
Cada mensaje que llegue se debe insertar en el servicio influx, teniendo en consideración que el **time** y **value** son *fields* y **version** es un *tag*.
Este mensaje se guardará en el bucket **system** en el measurement **dispositivos**.