from decoder import process_json
import json
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
    buffer = Buffer(samples_per_axis)
    
    for i in range(6):
        input("({}/6) Preapare band to calibrate {} axis and press enter.".format(i+1, CALIBRATION_MESSAGES[i]))
        collect_data(axis=i, buffer=buffer)
            
    buffer.print()

if __name__ == "__main__":
    config = read_config()
    calibrate(config)
