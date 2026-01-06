from fastapi import FastAPI, WebSocket
import json, asyncio
import requests
from datetime import datetime

app = FastAPI()



clients = {}
DJANGO_URL = "http://10.20.251.74:8001/receive/"

@app.websocket("/ws")
async def web_socket_endpoint(websocket: WebSocket):
    await websocket.accept()
    esp_id = None
    
    while True:
        try:
            
            data = await websocket.receive_text()
            json_data = json.loads(data)
            try:
                if "esp_id" in json_data:
                    esp_id = str(json_data.get("esp_id"))
                    clients[esp_id] = websocket
                    print(f"client d'id {esp_id} connecté")
                    continue
                try:
                    json_data["id"] = esp_id
                    reponse = requests.post(DJANGO_URL,json=json_data)
                    
                    print("*******************")
                    print(f"donnée à envoyer: {json_data}")
                    print(f"réponse de l'envoie vers django: {reponse.text} ")

                except Exception as e:
                    print(f"erreur envoie vers django : {e}")

            except json.JSONDecodeError:
                print(f"text reçu: {data}")    
           
            #await websocket.send_text("bonjour depuis l'API")
            #await asyncio.sleep(2)

        except Exception as e:
            
            print(f"client {esp_id} deconnecté")
            del clients[esp_id]
                
            break
            
                    

            

@app.post("/envoie/")
async def receive(requete: dict):
    cible = str(requete.get("esp_id"))
    print("*****django vers api****")
    print(f"envoie de django vers esp32: {requete}")
    print(f"cible: {cible}")
    print(f"ESP connectés: {list(clients.keys())}")

    if cible == "ALL":
        for cible, ws in clients.items():
            await ws.send_json(requete)
            print(f"Donnés envoyé à tous")
            return {"status": "ok"}

    elif cible in clients:
        await clients[cible].send_json(requete)
        print(f"Donnés envoyé à {cible}")
        return {"status": "ok"}
    else:
        print("Aucun ESP correspondant trouvé")
        return {"message": "aucun esp trouvé"}
    

