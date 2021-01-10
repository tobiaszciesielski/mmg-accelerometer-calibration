import json 
import base64
import struct
import numpy as np
from operator import itemgetter

BYTES_PER_SAMPLE = 2
DATA_FRAME_LENGTH = 18

def decode_json(raw_json):
  decoded = json.loads(raw_json)
  return itemgetter('data', 'timestamp', 'freq', 'packets', 'channels')(decoded)

def decode_data_frame(frame) -> np.ndarray: 
  decoded = base64.b64decode(frame)
  # '<' little endian, 'h' short
  return [struct.unpack("<h", decoded[i:i+BYTES_PER_SAMPLE])[0] for i in range(0, DATA_FRAME_LENGTH, BYTES_PER_SAMPLE)]

def tag_packet(packet, timestamp) -> dict:
  packet_data = np.array([decode_data_frame(frame) for frame in packet])
  return {"timestamp":timestamp, "data":packet_data}

def calc_interval_between_jsons(freq) -> int:
  return round(((1.0/freq)*1e6))

def calc_interval_between_packets(json_interval, packet_count):
  return round(json_interval/packet_count)

def get_accelerometer_features(samples) -> np.ndarray:
  squared = np.square(samples[:,:,0:3])
  sums = np.sum(squared, axis=2, keepdims=True, dtype=int)
  rooted = np.sqrt(sums)
  means = np.mean(rooted, axis=0)
  return np.reshape(means, 8)

def process_message(raw_json):
  packets, timestamp, freq, packets_count, channels_count = decode_json(raw_json)
  timestamp = round(timestamp,-4)
  print(timestamp)

  json_interval = calc_interval_between_jsons(freq)
  packets_interval = calc_interval_between_packets(json_interval, packets_count)

  timestamp-=json_interval
  for packet in packets:
    timestamp += packets_interval
    print(packet)
    yield tag_packet(packet, timestamp)


# 1, 2, 3, 4, 5
# 10, 20, 30, 40, 50

# {"data": 1, "timestamp": 10}, ... 

# TODO 
# # wspólna klasa do uczenia
# każdy rms wartość podzielić przez 4096