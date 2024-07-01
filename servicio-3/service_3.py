from flask import Flask, request, jsonify
from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta
import mysql.connector
import json

app = Flask(__name__)

# Configuración de InfluxDB
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "GFXIISVUqdA3N8CzcjN_EtZ50lAgeMO_VxJiYKWL1o2AC2DwQO33iSWix8Iy14Un1rtY2ZAgFhb62JZ7TqTbDA=="
INFLUXDB_ORG = "tecnoandina"
BUCKET = "system"
MEASUREMENT = "dispositivos"

# Configuración de MySQL
MYSQL_HOST = "localhost"
MYSQL_USER = "admin"
MYSQL_PASSWORD = "admin2024"
MYSQL_DATABASE = "challenge"

# Inicialización del cliente InfluxDB
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = influx_client.query_api()

# Inicialización del cliente MySQL
mysql_conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
mysql_cursor = mysql_conn.cursor()

def process_data(version, time_search):
    try:
        # Convertir el tiempo de búsqueda a timedelta
        unit = time_search[-1]
        value = int(time_search[:-1])
        if unit == 'm':
            time_delta = timedelta(minutes=value)
        elif unit == 'h':
            time_delta = timedelta(hours=value)
        elif unit == 'd':
            time_delta = timedelta(days=value)
        else:
            return jsonify({"status": "No se pudo procesar los parámetros"}), 422

        # Obtener la fecha y hora actuales
        end_time = datetime.now()
        start_time = end_time - time_delta

        # Consulta a InfluxDB
        query = f'''
        from(bucket: "{BUCKET}")
        |> range(start: {start_time.isoformat()}Z, stop: {end_time.isoformat()}Z)
        |> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")
        |> filter(fn: (r) => r["version"] == "{version}")
        '''
        result = query_api.query(org=INFLUXDB_ORG, query=query)

        alerts = []

        # Procesar los resultados
        for table in result:
            for record in table.records:
                value = record.get_value()
                alert_type = None
                if version == 1:
                    if value > 800:
                        alert_type = "ALTA"
                    elif value > 500:
                        alert_type = "MEDIA"
                    elif value > 200:
                        alert_type = "BAJA"
                elif version == 2:
                    if value < 200:
                        alert_type = "ALTA"
                    elif value < 500:
                        alert_type = "MEDIA"
                    elif value < 800:
                        alert_type = "BAJA"

                if alert_type:
                    alerts.append((record.get_time(), value, version, alert_type))

        # Insertar alertas en MySQL
        for alert in alerts:
            mysql_cursor.execute(
                "INSERT INTO alerts (datetime, value, version, type, sended) VALUES (%s, %s, %s, %s, %s)",
                (alert[0], alert[1], alert[2], alert[3], False)
            )

        mysql_conn.commit()

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": f"Error: {e}"}), 500


def search_alerts(version, alert_type=None, sended=None):
    try:
        query = "SELECT datetime, value, version, type, sended FROM alerts WHERE version = %s"
        params = [version]

        if alert_type:
            query += " AND type = %s"
            params.append(alert_type)

        if sended is not None:
            query += " AND sended = %s"
            params.append(sended)

        mysql_cursor.execute(query, tuple(params))
        result = mysql_cursor.fetchall()

        alerts = [
            {
                "datetime": alert[0],
                "value": alert[1],
                "version": alert[2],
                "type": alert[3],
                "sended": alert[4]
            }
            for alert in result
        ]

        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({"status": f"Error: {e}"}), 500


def send_alerts(version, alert_type):
    try:
        query = "SELECT id_alerta FROM alerts WHERE version = %s AND type = %s AND sended = FALSE"
        params = (version, alert_type)

        mysql_cursor.execute(query, params)
        result = mysql_cursor.fetchall()

        for alert in result:
            mysql_cursor.execute(
                "UPDATE alerts SET sended = TRUE WHERE id_alerta = %s", (alert[0],)
            )

        mysql_conn.commit()

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": f"Error: {e}"}), 500


@app.route('/challenge/process', methods=['POST'])
def process():
    data = request.json
    version = data.get("version")
    time_search = data.get("timeSearch")
    if not version or not time_search:
        return jsonify({"status": "No se pudo procesar los parámetros"}), 422
    return process_data(version, time_search)


@app.route('/challenge/search', methods=['POST'])
def search():
    data = request.json
    version = data.get("version")
    alert_type = data.get("type")
    sended = data.get("sended")
    if not version:
        return jsonify({"status": "No se pudo procesar los parámetros"}), 422
    return search_alerts(version, alert_type, sended)


@app.route('/challenge/send', methods=['POST'])
def send():
    data = request.json
    version = data.get("version")
    alert_type = data.get("type")
    if not version or not alert_type:
        return jsonify({"status": "No se pudo procesar los parámetros"}), 422
    return send_alerts(version, alert_type)


if __name__ == '__main__':
    app.run(debug=True)
