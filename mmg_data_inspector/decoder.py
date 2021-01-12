import json 
import base64
import struct
from typing import Generator
import numpy as np
from operator import itemgetter

BYTES_PER_SAMPLE = 2
DATA_FRAME_LENGTH = 18

with open("calibration_params.json") as file:
    config = json.load(file)

ZERO_PARAM =  np.transpose(np.array([config['X_0'], config['Y_0'], config['Z_0']]))
K_PARAM = np.transpose(np.array([config['X_k'], config['Y_k'], config['Z_k']]))

def process_json(json_message: str) -> Generator:
  package, timestamp, freq, packets_count, channels_count = decode_json(json_message)
  for packet in package:
    decoded = decode_packet(packet)
    calibrated = calibrate_accelerometer(decoded)
    yield calibrated

def decode_json(raw_json):
  decoded = json.loads(raw_json)
  return itemgetter('data', 'timestamp', 'freq', 'packets', 'channels')(decoded)

def decode_packet(packet) -> np.ndarray:
  packet = np.array([decode_sample(sample) for sample in packet], dtype=float)
  return packet

def decode_sample(sample) -> np.ndarray: 
  decoded = base64.b64decode(sample)
  # '<' little endian, 'h' short
  return [struct.unpack("<h", decoded[i:i+BYTES_PER_SAMPLE])[0] for i in range(0, DATA_FRAME_LENGTH, BYTES_PER_SAMPLE)]

def calibrate_accelerometer(packet) -> np.ndarray:
  packet[:,0:3] = (packet[:,0:3]-ZERO_PARAM)/K_PARAM
  return packet
