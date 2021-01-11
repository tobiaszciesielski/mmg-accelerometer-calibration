import json
import paho.mqtt.client as mqtt
from decoder import process_json
from buffer import Buffer

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

buffer = Buffer(SAMPLES_PER_AXIS)
packet_counter = 0

CALIBRATION_MESSAGES = [
    "Xmin",
    "Xmax",
    "Ymin",
    "Ymax",
    "Zmin",
    "Zmax",
]

# ================

def connect_to_broker(client:mqtt.Client):
    client.connect(BROKER_IP, BROKER_PORT)


def stop_stream(client:mqtt.Client):
    client.publish(CONTROL_TOPIC, "stop")


def start_stream(client:mqtt.Client):
    client.publish(CONTROL_TOPIC, "start")


def on_message(client:mqtt.Client, userdata, msg):
  global packet_counter, buffer

  package = process_json(str(msg.payload.decode('utf-8')))
  
  for packet in package: 
    if packet_counter == SAMPLES_PER_AXIS:
        stop_stream(client)
        client.disconnect()
    elif packet_counter < SAMPLES_PER_AXIS:
        buffer.append(packet)

    packet_counter+=1


def calibrate():
    global packet_counter

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = lambda c, userdata, flags, rc: c.subscribe(DATA_STREAM_TOPIC)
    mqtt_client.on_message = on_message
    connect_to_broker(mqtt_client)
    
    for i in range(6):
        packet_counter = 0    
        input("({}/6) Prepare {} axis and press enter.".format(i+1, CALIBRATION_MESSAGES[i]))
        print("Collecting data...")
        connect_to_broker(mqtt_client)
        start_stream(mqtt_client)
        mqtt_client.loop_forever()

    stop_stream(mqtt_client)
    mqtt_client.disconnect()
    
    # with open("result.json", 'w') as file:
    #     file.write()
    print("Calibration completed.")
    buffer.save()
    


if __name__ == "__main__":
    calibrate()
