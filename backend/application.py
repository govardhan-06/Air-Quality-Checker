import os
from fastapi import FastAPI
from paho.mqtt import client as mqtt_client
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet
from supabase_config import Supabase

load_dotenv()
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MQTT Configuration
broker = os.getenv("MQTT_BROKER_IP")
port = int(os.getenv("MQTT_PORT"))
topic = os.getenv("SUB_TOPIC")
mqtt_user = os.getenv("MOSQUITTO_USERNAME")
mqtt_password = os.getenv("MOSQUITTO_PASSWORD")

key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(key)

supa_client=Supabase()

# Store received data
received_data: List[dict] = []

# MQTT Callback function to handle incoming messages
def on_message(client, userdata, message):
    try:
        # Decrypt the received message
        encrypted_payload = message.payload
        decrypted_payload = cipher.decrypt(encrypted_payload).decode()

        # Split the decrypted payload into data parts (SensorID, Location, CO2, PM2.5, NO2)
        data_parts = decrypted_payload.split('&')
        sensor_id = data_parts[0].split('=')[1].strip()
        location = data_parts[1].split('=')[1].strip()
        co2 = float(data_parts[2].split('=')[1].strip().replace("ppm", ""))
        pm25 = float(data_parts[3].split('=')[1].strip().replace("µg/m³", ""))
        no2 = float(data_parts[4].split('=')[1].strip().replace("ppb", ""))

        # Create a dictionary for the received air quality data
        payload = {
            "sensor_id": sensor_id,
            "location": location,
            "co2_level": co2,
            "pm25_level": pm25,
            "no2_level": no2
        }

        supa_client.insert_item(payload)

        # Store the received data
        received_data.append(payload)
        print(f"Received Encrypted payload: {encrypted_payload}")
        print(f"Received MQTT message: {payload}")

    except Exception as e:
        print(f"Error processing message: {e}")

# Connect to MQTT broker
def connect_mqtt():
    client = mqtt_client.Client(protocol=mqtt_client.MQTTv311)
    client.username_pw_set(mqtt_user, mqtt_password)
    client.on_message = on_message

    try:
        client.connect(broker, port)
        print("Connected to MQTT broker successfully")
        client.subscribe(topic)  # Subscribe after connecting
        print(f"Subscribed to topic: {topic}")
        client.loop_start()  # Start the MQTT client loop
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

    return client

@app.get("/air-quality/latest")
async def get_air_quality():
    '''
    Returns the latest air quality data.
    '''
    if received_data:
        return JSONResponse(content=received_data[-1], status_code=200)
    else:
        return JSONResponse(content={"error": "No air quality data available"}, status_code=404)

@app.get("/air-quality/history")
async def get_air_quality_history():
    '''
    Returns a list of all received air quality data (latest 30 records).
    '''
    try:
        fetched_data = supa_client.fetch_item(30)
        return JSONResponse(content=fetched_data, status_code=200)
    except:
        return JSONResponse(content={"error": "Failed to fetch air quality data"}, status_code=500)

# Connect the MQTT client
mqtt_client_instance = connect_mqtt()

# Run the FastAPI app
if __name__ == "__main__":    
    uvicorn.run(app, host="0.0.0.0", port=8000)
