#include <WiFi.h>
#include <Wire.h>
#include <ArduinoWebsockets.h>
#include <ArduinoJson.h>

using namespace websockets;

/* ================= CONFIG ================= */

const char* ssid = "Xiaomi";
const char* password = "11111111";

const char* server = "10.20.251.74";
const uint16_t port = 8000;
const char* ws_path = "/ws";

#define STM32_ADDR 0x0C   // Adresse I2C STM32 (7 bits)

/* ================= OBJETS ================= */

WebsocketsClient client;

/* ================= VARIABLES ================= */

float temperature = 0.0;
float tension = 0.0;

/* ================= WEBSOCKET CALLBACK ================= */

void onMessageCallback(WebsocketsMessage message)
{
  Serial.print("Message WS reçu: ");
  Serial.println(message.data());

  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, message.data());

  if (error) {
    Serial.println("Erreur JSON");
    return;
  }

  if (!doc.containsKey("temperature") || !doc.containsKey("tension")) {
    Serial.println("Champs manquants");
    return;
  }

  temperature = doc["temperature"];
  tension = doc["tension"];

  Serial.printf("Temp=%.2f°C | Tension=%.2fV\n", temperature, tension);

  sendToSTM32();
}

/* ================= I2C SEND ================= */

void sendToSTM32()
{
  uint8_t buffer[8];

  memcpy(&buffer[0], &temperature, 4);
  memcpy(&buffer[4], &tension, 4);

  Wire.beginTransmission(STM32_ADDR);
  Wire.write(buffer, 8);
  uint8_t status = Wire.endTransmission();

  if (status == 0) {
    Serial.println("I2C → STM32 OK");
  } else {
    Serial.print("Erreur I2C : ");
    Serial.println(status);
  }
}

/* ================= WIFI ================= */

void connectWiFi()
{
  WiFi.begin(ssid, password);
  Serial.print("Connexion WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println("\nWiFi connecté !");
}

/* ================= WEBSOCKET ================= */

void connectWebSocket()
{
  client.onMessage(onMessageCallback);

  Serial.print("Connexion WebSocket");
  while (!client.connect(server, port, ws_path)) {
    Serial.print(".");
    delay(1000);
  }

  // Identification ESP
  StaticJsonDocument<100> doc;
  doc["esp_id"] = 66;
  String data;
  serializeJson(doc, data);
  client.send(data);

  Serial.println("\nWebSocket connecté : " + data);
}

/* ================= SETUP ================= */

void setup()
{
  Serial.begin(115200);
  delay(1000);

  connectWiFi();
  connectWebSocket();

  // I2C Master
  Wire.begin(21, 22);   // SDA, SCL
  Wire.setClock(100000); // 100 kHz

  Serial.println("ESP32 prêt");
}

/* ================= LOOP ================= */

void loop()
{
  client.poll();

  if (!client.available()) {
    Serial.println("WebSocket perdu → reconnexion");
    connectWebSocket();
  }

  delay(10);
}
