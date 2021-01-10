import json
import paho.mqtt.client as mqtt
from decoder import decode_json

def on_message(client, userdata, msg):
    packets= decode_json(str(msg.payload.decode('utf-8')))
    for packet in packets:
      buffer.append(sample)

client = mqtt.Client()
client.on_connect = lambda client, userdata, flags, rc: client.subscribe("sensors/data/mmg")
client.on_message = on_message

client.connect("192.168.1.26", 1883, 60)
client.loop_forever()
