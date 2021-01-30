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

def save_to_file(params):
    with open("calibration_params.json", 'w') as file:
        file.write(json.dumps(params))

def compute_calibration_params():
    
    import numpy as np

    def find_zero(a, b):
        return (a + b) / 2 

    def count_k(a, b):
        return (b - a) / 2

    buffer.save()

    accelerometer_values = buffer.get_all()[:,:,:,0:3]
    extreme_values = np.round(np.mean(accelerometer_values, axis=1, dtype=int))
    Xmin = extreme_values[0,:,0]
    Xmax = extreme_values[1,:,0]
    Ymin = extreme_values[2,:,1]
    Ymax = extreme_values[3,:,1]
    Zmin = extreme_values[4,:,2]
    Zmax = extreme_values[5,:,2]

    X_zero = find_zero(Xmin, Xmax)
    X_k = count_k(Xmin, Xmax)

    Y_zero = find_zero(Ymin, Ymax)
    Y_k = count_k(Ymin, Ymax)

    Z_zero = find_zero(Zmin, Zmax)
    Z_k = count_k(Zmin, Zmax)

    dict_to_json = {
        "X_0":np.round(X_zero).tolist(),
        "Y_k":np.round(Y_k).tolist(),
        "Y_0":np.round(Y_zero).tolist(),
        "X_k":np.round(X_k).tolist(),
        "Z_0":np.round(Z_zero).tolist(),
        "Z_k":np.round(Z_k).tolist(),
    }
    
    return dict_to_json


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
    
    
    print("Computing parameters...")
    params = compute_calibration_params()


    print("Saving to file...")
    save_to_file(params)

    print("Calibration completed.")
    


if __name__ == "__main__":
    calibrate()
