import paho.mqtt.client as mqtt
import random
import time
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

# MQTT Configuration
mqtt_server = os.getenv("MQTT_BROKER_IP")
mqtt_port = int(os.getenv("MQTT_PORT"))
mqtt_user = os.getenv("MOSQUITTO_USERNAME")
mqtt_password = os.getenv("MOSQUITTO_PASSWORD")
topic = os.getenv("SUB_TOPIC")

key = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(key)

# List of random place names for location
locations = ["VIT CHENNAI"]

# Generate simulated air quality data with sensor ID and random location
def generate_air_quality_data():
    sensor_id = random.randint(1000, 9999)  # Simulated sensor ID
    location = random.choice(locations)     # Randomly chosen location
    
    co2 = random.uniform(400, 5000)  # Simulated CO2 level in ppm
    pm25 = random.uniform(0, 500)    # Simulated PM2.5 level in µg/m³
    no2 = random.uniform(0, 200)     # Simulated NO2 level in ppb
    
    return f"SensorID={sensor_id} & Location={location} & CO2={co2:.2f}ppm & PM2.5={pm25:.2f}µg/m³ & NO2={no2:.2f}ppb"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

def publish_air_quality_data(client):
    while True:
        air_quality_data = generate_air_quality_data()

        # Encrypt the air quality data
        encrypted_data = cipher.encrypt(air_quality_data.encode())

        result = client.publish(topic, encrypted_data)
        status = result.rc
        if status == 0:
            print(f"Data sent: {air_quality_data}")
            print(f"Data Encrypted: {encrypted_data}")
        else:
            print(f"Failed to send message: {status}")
        time.sleep(5)  # Send data every 5 seconds

client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.on_connect = on_connect

try:
    client.connect(mqtt_server, mqtt_port, 60)
    client.loop_start()  # Start the loop in a separate thread
    publish_air_quality_data(client)  # Start publishing air quality data
except Exception as e:
    print(f"Connection error: {e}")
