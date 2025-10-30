from fastapi import FastAPI, WebSocket
import json, asyncio
import requests
from datetime import datetime

app = FastAPI()

client = None


DJANGO_URL = "http://10.69.211.74:8001/receive/"

@app.websocket("/ws")
async def web_socket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global client
    client = websocket
    while True:
        try:
            #now = datetime.now().strftime("%H:%M:%S")
            
            data = await websocket.receive_text()
            json_data = json.loads(data)
            try:
                #json_data["date"] = now
                #print(f"donnés reçues: {json_data}")
                try:
                    reponse = requests.post(DJANGO_URL,json=json_data)
                    print("*******************")
                    print(f"réponse de l'envoie vers django: {reponse.status_code} ")

                except Exception as e:
                    print(f"erreur envoie vers django : {e}")

            except json.JSONDecodeError:
                print(f"text reçu: {data}")    
           
            #await websocket.send_text("bonjour depuis l'API")
            #await asyncio.sleep(2)

        except Exception as e:
            print(f"connexion websocket fermé: {e}")
            break

@app.post("/envoie")
async def receive(requete: dict):
    global client
    print("*****django vers api****")
    print(f"envoie de django vers esp32: {requete}")
    if client:
        await client.send_json(requete)
    return {"status": "ok"}

