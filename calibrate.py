import json
from json.decoder import JSONDecodeError
import paho.mqtt.client as mqtt

from circularBuffer import Circular_Buffer
from preprocess import get_accelerometer_features, process_message

circular_buffer = Circular_Buffer(500, dict, {})

def on_message(client, userdata, msg):
  try:
    prepared_samples = process_message(str(msg.payload.decode('utf-8')))
    for sample in prepared_samples:
      circular_buffer.append(sample)
      if circular_buffer.get_portion_size(time_window=2000000) >= 100:
        print(json.dumps(get_accelerometer_features(circular_buffer.get_portion(time_window=2000000, stride=100))))
  except JSONDecodeError:
    print('Json decode error.')

client = mqtt.Client()
client.on_connect = lambda client, userdata, flags, rc: client.subscribe("test")
client.on_message = on_message

client.connect("192.168.8.105", 1883, 60)
client.loop_forever()
