// arduino_sensors.ino
#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Pines para LEDs
int ledCargaPin = 9;
int ledSolarPin = 8;  // Opcional - para indicar energía solar

// Simulación de variables de energía
unsigned long lastEnergyUpdate = 0;
int consumoActual = 100;
float voltajeBateria = 3.8;  // Valor simulado - ajustar según medición real

void setup() {
  Serial.begin(9600);
  dht.begin();
  //pinMode(A0, INPUT);  // Sensor voltaje batería
  //pinMode(9, OUTPUT);  // LED simulación carga
  //Serial.println("🔍 PRUEBA DHT11 - Enviando datos...");
  Serial.println("✅ Sistema Energía Solar PERU - Con TP4056 y LEDs");
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  //int voltaje = analogRead(A0);
  //int consumo = random(50, 200);  // Simulación consumo

  // SIMULAR DATOS DE ENERGÍA (puedes conectar sensor real después)
  simularEnergia();
  
  // Formato para fácil parsing en Python
  Serial.print("TEMP:");
  Serial.print(temp);
  Serial.print("|HUM:");
  Serial.print(hum);
  //Serial.print("|VOLT:");
  //Serial.print(voltajeBateria * 100);  // Multiplicar por 100 para evitar decimales
  Serial.print("|BATT:");
  Serial.print(int(voltajeBateria * 100));
  Serial.print("|CONS:");
  Serial.println(consumoActual);
  
  digitalWrite(9, HIGH);  // Simular carga
  delay(1000);
  digitalWrite(9, LOW);
  //delay(4000);

  // CONTROLAR LEDs
  controlarLEDs();
  
  delay(5000);  // 5 segundos entre lecturas
}

void simularEnergia() {
  // Simular variaciones en consumo y voltaje
  consumoActual = 80 + random(70);  // Consumo entre 80-150 mA
  
  // Simular voltaje de batería (3.6V - 4.2V para Li-ion)
  voltajeBateria = 3.7 + (random(0, 50) / 100.0);
}

void controlarLEDs() {
  // LED de CARGA (Pin 9) - parpadeo rápido indicando actividad
  digitalWrite(ledCargaPin, HIGH);
  delay(100);
  digitalWrite(ledCargaPin, LOW);
  
  // LED SOLAR (Pin 8) - encendido si hay "buen" voltaje
  if (voltajeBateria > 3.8) {
    digitalWrite(ledSolarPin, HIGH);  // Batería bien cargada
  } else {
    digitalWrite(ledSolarPin, LOW);   // Batería baja
  }
}
