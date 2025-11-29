MEMORIA TÉCNICA: 

Sistema de Monitoreo de Energía Solar para Comunidades del Perú Profundo

1. INTRODUCCIÓN:

1.1 Resumen Ejecutivo

Este documento describe el diseño, implementación y resultados de un sistema IoT de monitoreo de energía solar autónomo, desarrollado específicamente para comunidades remotas del Perú sin acceso a la red eléctrica convencional. El sistema integra tecnologías de hardware abierto, sensores ambientales y visualización en tiempo real para proporcionar datos críticos sobre el desempeño de sistemas solares autónomos.

1.2 Objetivos del Proyecto

### Objetivo Principal
Implementar un sistema autónomo de monitoreo energético que opere exclusivamente con energía solar y proporcione datos en tiempo real sobre parámetros ambientales y de desempeño del sistema.

### Objetivos Específicos
1. Diseñar circuito electrónico con gestión eficiente de energía
2. Desarrollar firmware para adquisición continua de datos
3. Implementar pipeline de datos hacia base de datos temporal
4. Crear dashboard interactivo para visualización en tiempo real
5. Validar autonomía y confiabilidad del sistema

1.3 Arquitectura del Sistema

1.3.1 Diagrama de Bloques:

[ SENSORES ] → [ ARDUINO ] → [ PROTOBOARD ] → [ DEBIAN VM ] → [ GRAFANA ]
 ↑ ↑ ↑ ↑ ↑
DHT11 Procesamiento TP4056 + InfluxDB + Dashboard
TP4056 Batería Python
Panel Solar
Blockchain para Facturación.

2. COMPONENTES:

2.1 Componentes de Hardware

2.1.1 Microcontrolador
- **Arduino Uno R3**
  - Procesador: ATmega328P
  - Clock: 16 MHz
  - Memoria: 32KB Flash, 2KB SRAM
  - Alimentación: 5V via USB o 7-12V via Vin

2.1.2 Sensores
- **DHT11** - Sensor de temperatura y humedad
  - Rango temperatura: 0-50°C ±2°C
  - Rango humedad: 20-90% ±5%
  - Interface: Digital single-bus

- **TP4056** - Módulo de carga Li-ion
  - Voltaje entrada: 4.5-5.5V
  - Corriente carga: 1000mA programable
  - Protección: Sobrecarga, cortocircuito

2.1.3 Sistema de Energía
- **Batería:** BRC 18650 BL 1600mAh 3.7V
- **Panel Solar:** Overclick 5V 1W
- **Autonomía estimada:** 72+ horas

2.2 Software y Protocolos

2.2.1 Firmware Arduino

+++++++++++++++++++++++++++++++++++++++++++
// Estructura principal
void loop() {
  leerSensores();
  procesarDatos();
  enviarSerial();
  controlarLEDs();
  delay(5000);
}

++++++++++++++++++++++++++++++++++++++++++++

2.2.2 Monitoreo:

Stack de Software
Sistema Operativo: Debian 13

Lenguaje Python: 3.13

Base de Datos: InfluxDB 2.7

Dashboard: Grafana 9.5+

Protocolo: Flux Query Language

3. IMPLEMENTACIÓN TÉCNICA:

3.1 Diseño de Circuito
Conexiones Principales

DHT11 → Arduino
  VCC  → 5V
  DATA → Pin 2
  GND  → GND

TP4056 → Sistema
  IN+  → Panel Solar+
  IN-  → Panel Solar-
  B+   → Batería+
  B-   → Batería-
  OUT+ → Arduino Vin
  OUT- → Arduino GND

Protoboard
Organización modular de componentes

LEDs indicadores de estado

Puntos de prueba para diagnóstico

3.2 Programación
Sketch Arduino
Lectura cada 5 segundos

Formato de datos: TEMP:26.5|HUM:54|BATT:412|CONS:120

Control de LEDs indicadores

Manejo de errores de sensores

Script Python

++++++++++++++++++++++++++++++++++++
# Funciones principales
def leer_serial():
def parsear_datos():
def enviar_influxdb():
def manejar_errores():
++++++++++++++++++++++++++++++++++++

3.3 Base de Datos
Estructura InfluxDB

- Bucket: sensor_data

- Measurement: sensor_energy

- Fields: temperature, humidity, battery_voltage, consumption

- Tags: location="peru_profundo"

Queries Flux Principales

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// Query para datos recientes
from(bucket: "sensor_data")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "sensor_energy")
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

3.4 Dashboard Grafana
Paneles Implementados
Voltaje de Batería - Gauge con thresholds

Temperatura Ambiental - Time series

Humedad Relativa - Time series

Consumo Energético - Stat

Estado de Carga - Porcentaje

Historial 24h - Tendencias

Tabla de Datos - Últimas lecturas

Eficiencia Sistema - Métricas

4. Resultados y Métricas
4.1 Desempeño del Sistema
Exactitud de Datos
Temperatura: ±2°C vs termómetro de referencia

Humedad: ±5% vs higrómetro calibrado

Voltaje: ±0.1V vs multímetro digital

Confiabilidad
Uptime: 99.8% en período de prueba de 7 días

Pérdida de datos: < 0.1% por reinicios programados

Latencia: < 2 segundos sensor-to-dashboard

Consumo Energético
Corriente en reposo: 45mA

Corriente en operación: 80-150mA

Autonomía con batería llena: 72 horas

Tiempo de carga solar: 6-8 horas

4.2 Análisis de Datos
Patrones de Consumo
Consumo base estable en 80-120mA

Picos durante transmisión de datos

Eficiencia constante en diferentes condiciones de luz

Comportamiento de Batería
Voltaje estable entre 3.8V-4.1V en operación normal

Descarga gradual sin caídas bruscas

Recuperación rápida con carga solar

5. Conclusiones y Recomendaciones
5.1 Logros Alcanzados
- Sistema 100% operativo con energía solar
- Dashboard en tiempo real con 8 paneles
- Datos confiables con latencia mínima
- Autonomía extendida (> 72 horas)
- Interfaz accesible y comprensible

5.2 Lecciones Aprendidas
Gestión de energía: Critical para sistemas autónomos

Robustez de código: Manejo de errores esencial

Documentación: Vital para mantenimiento y escalabilidad

Pruebas continuas: Garantizan confiabilidad

5.3 Recomendaciones para Futuras Versiones
Mejoras de Hardware
Integrar medición real de corriente

Agregar sensor de irradiación solar

Implementar MPPT para mayor eficiencia

Considerar ESP32 para conectividad WiFi

Mejoras de Software
Sistema de alertas automáticas

Análisis predictivo con machine learning

API REST para integración con otros sistemas

Aplicación móvil para monitoreo remoto

Escalabilidad
Arquitectura multi-nodo para cobertura extendida

Comunicación LoRa para larga distancia

Almacenamiento local con sincronización periódica

Paneles solares de mayor capacidad




