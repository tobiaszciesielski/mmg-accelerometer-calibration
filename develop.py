import json
import paho.mqtt.client as mqtt
from decoder import process_json
from buffer import Buffer


CALIBRATION_MESSAGES = [
    "Xmin",
    "Xmax",
    "Ymin",
    "Ymax",
    "Zmin",
    "Zmax",
]


def read_config():
    with open("./config.json") as file:
        return json.load(file)


packet_counter = 0
def on_message(client, userdata, msg):
  global packet_counter

  package = process_json(str(msg.payload.decode('utf-8')))
  for packet in package:
    packet_counter+=1
    if packet_counter == 100:
      client.publish("sensors/control/mmg", "stop")
      print("INTERVAL")
      # client.publish("sensors/control/mmg", "start")
      packet_counter=0
    print(packet_counter)


def collect_data(axis:int, buffer:Buffer): 
    counter = 0
    while True:
        fake_data = input("enter fake data:")
        package = process_json(fake_data)
        for packet in package:
            if not buffer.append(axis, packet):
                return
            else:
                counter+=1
                print(counter)


def calibrate(config:dict):
    samples_per_axis = config["samples_per_axis"]
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = lambda c, userdata, flags, rc: c.subscribe("sensors/data/mmg")
    mqtt_client.on_message = on_message
    mqtt_client.connect("192.168.1.26", 1883, 60)
    mqtt_client.publish("sensors/control/mmg", "start")
    mqtt_client.loop_forever()
    # buffer = Buffer(samples_per_axis)
    
    for i in range(6):
        input("({}/6) Preapare band to calibrate {} axis and press enter.".format(i+1, CALIBRATION_MESSAGES[i]))
        mqtt_client.publish("sensors/control/mmg", "start")
        # collect_data(axis=i, buffer=buffer)
        
    mqtt_client.publish("sensors/control/mmg", "stop")
    # buffer.print()


if __name__ == "__main__":
    config = read_config()
    calibrate(config)
