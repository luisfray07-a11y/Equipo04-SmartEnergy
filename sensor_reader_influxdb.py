# sensor_reader_influxdb.py
import serial
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException

# CONFIGURACIÓN
token = "XNXh3CGCMq47qqRuZ__EbpxFm7UNeflvia5IEwAGiT7fMuK7_bijdI5-HMixErgknnL50VoOdD4hlH2vKL4nYA=="
org = "energia_peru"
bucket = "sensor_data"
url = "http://localhost:8086"

def setup_influxdb():
    """Configurar cliente InfluxDB con verificación"""
    try:
        client = InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        # Verificar conexión
        health = client.health()
        print(f"✅ InfluxDB conectado: {health.status}")
        return client, write_api
    except Exception as e:
        print(f"❌ Error conectando a InfluxDB: {e}")
        return None, None

def parse_arduino_data(line):
    """Función separada para parsing robusto"""
    try:
        print(f"🔍 Parseando: {line}")
        data = {}
        parts = line.strip().split('|')
        
        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                # BATT como entero, otros según contenido
                if key == 'BATT':
                    data[key] = int(float(value))  # Convertir a entero
                else:
                    data[key] = float(value) if '.' in value else int(value)
        
        print(f"✅ Datos parseados: {data}")
        return data
    except Exception as e:
        print(f"❌ Error en parsing: {e}")
        return None

def main():
    client, write_api = setup_influxdb()
    if not client:
        return
    
    # Conectar Arduino
    try:
        arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        time.sleep(2)
        print("✅ Arduino conectado")
    except Exception as e:
        print(f"❌ Error con Arduino: {e}")
        return

    error_count = 0
    max_errors = 5
    
    while True:
        try:
            if arduino.in_waiting > 0:
                line = arduino.readline().decode('utf-8').strip()
                print(f"📨 Raw: {line}")

                if line and line.startswith('TEMP'):
                    # Usar la función de parsing separada
                    data = parse_arduino_data(line)
                    
                    if data and 'TEMP' in data and 'HUM' in data and 'BATT' in data and 'CONS' in data:
                        # Crear punto para InfluxDB
                        point = Point("sensor_energy")\
                            .tag("location", "peru_profundo")\
                            .field("temperature", data['TEMP'])\
                            .field("humidity", data['HUM'])\
                            .field("battery_voltage", data['BATT'])\
                            .field("consumption", data['CONS'])
                        
                        try:
                            # Intentar enviar a InfluxDB
                            write_api.write(bucket=bucket, org=org, record=point)
                            print(f"📊 Enviado: Temp={data['TEMP']}°C, Bat={data['BATT']}mV")
                            error_count = 0

                        except ApiException as e:
                            error_count += 1
                            print(f"⚠️ Error InfluxDB ({error_count}/{max_errors}): {e}")

                            if error_count >= max_errors:
                                print("🔴 MÁXIMOS ERRORES ALCANZADOS - Reconectando...")
                                client, write_api = setup_influxdb()
                                error_count = 0
                    else:
                        print("❌ Datos incompletos o parsing falló")

            time.sleep(2)

        except KeyboardInterrupt:
            print("\n🛑 Deteniendo...")
            break
        except Exception as e:
            print(f"❌ Error general: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()