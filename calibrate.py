import json
import paho.mqtt.client as mqtt
from decoder import process_json

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

c = mqtt.Client()
c.on_connect = lambda c, userdata, flags, rc: c.subscribe("sensors/data/mmg")
c.on_message = on_message
c.connect("192.168.1.26", 1883, 60)
c.publish("sensors/control/mmg", "start")
c.loop_forever()
