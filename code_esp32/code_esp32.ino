#include <WiFi.h>
#include <ArduinoWebsockets.h>
#include <ArduinoJson.h>

char* ssid = "Xiaomi";
char* pswd = "999999999";
char* server = "ws://10.69.211.74:8000/ws";
using namespace websockets; 


WebsocketsClient client;

void onMessageCallback(WebsocketsMessage message){
    Serial.print("message reçu: ");
    Serial.println(message.data());
  }

void connect_wifi(){

  WiFi.begin(ssid,pswd);
  Serial.print("connexion");
  while(WiFi.status()!= WL_CONNECTED){
    Serial.print(".");
    delay(500);
  }
  Serial.println("connexion réussie");

}
void connect_websocket(){
  Serial.print("connexion socket en cours");
  while(!client.connect(server)){
    Serial.print(".");
    delay(200);
  }
  client.onMessage(onMessageCallback);

  StaticJsonDocument<100> doc;
  doc["esp_id"] = 66;
  String data;
  serializeJson(doc, data);
  client.send(data);

  Serial.println("connexion socket réussie pour le client " + data);

}

void setup() {
  Serial.begin(115200);
  connect_wifi();
  connect_websocket();
}
unsigned long preMillis = 0;

void loop() {
  unsigned long currentMillis = millis();
 
  if(!client.available()){
    Serial.println("attente client");
    connect_websocket();
  }
  client.poll();
   if(currentMillis - preMillis >= 5000){
    preMillis = currentMillis;
    StaticJsonDocument<200> dict;
    String data;
    dict["temperature"] = random(1, 1000);
    dict["tension"] = random(1, 3000);
    serializeJson(dict, data);
    client.send(data);
  }
  
  delay(50);
  

}
