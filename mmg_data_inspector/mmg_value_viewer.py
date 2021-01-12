import json
import numpy as np
import paho.mqtt.client as mqtt
from decoder import process_json

def read_config():
    with open("./config.json", "r") as file:
        return json.load(file)

# ================
# GLOBAL VARIABLES

config = read_config()

SAMPLES_PER_AXIS = config["samples_per_axis"]
DATA_STREAM_TOPIC  = config["data_stream_topic"]
BROKER_IP = config["broker_ip"]
BROKER_PORT = config["broker_port"]
CONTROL_TOPIC = config["control_topic"]

CALIBRATION_MESSAGES = [
    "X",
    "-X",
    "Y",
    "-Y",
    "Z",
    "-Z",
]

# ================

def connect_to_broker(client:mqtt.Client):
    client.connect(BROKER_IP, BROKER_PORT)


def stop_stream(client:mqtt.Client):
    client.publish(CONTROL_TOPIC, "stop")


def start_stream(client:mqtt.Client):
    client.publish(CONTROL_TOPIC, "start")


def on_message(client:mqtt.Client, userdata, msg):
  package = process_json(str(msg.payload.decode('utf-8')))
  for packet in package: 
    print(packet)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = lambda c, userdata, flags, rc: c.subscribe(DATA_STREAM_TOPIC)
mqtt_client.on_message = on_message
connect_to_broker(mqtt_client)
start_stream(mqtt_client)
mqtt_client.loop_forever()
