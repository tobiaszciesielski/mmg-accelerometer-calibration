import json 
import base64
import struct
from typing import Generator
import numpy as np
from operator import itemgetter

BYTES_PER_SAMPLE = 2
DATA_FRAME_LENGTH = 18

def process_json(json_message: str) -> Generator:
  package, timestamp, freq, packets_count, channels_count = decode_json(json_message)
  for packet in package:
    yield decode_packet(packet)

def decode_json(raw_json):
  decoded = json.loads(raw_json)
  return itemgetter('data', 'timestamp', 'freq', 'packets', 'channels')(decoded)

def decode_packet(packet) -> np.ndarray:
  packet = np.array([decode_sample(sample) for sample in packet])
  return packet

def decode_sample(sample) -> np.ndarray: 
  decoded = base64.b64decode(sample)
  # '<' little endian, 'h' short
  return [struct.unpack("<h", decoded[i:i+BYTES_PER_SAMPLE])[0] for i in range(0, DATA_FRAME_LENGTH, BYTES_PER_SAMPLE)]
