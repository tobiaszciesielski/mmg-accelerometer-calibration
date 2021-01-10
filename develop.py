import numpy as np

calibration_messages = [
    "Xmin",
    "Xmax",
    "Ymin",
    "Ymax",
    "Zmin",
    "Zmax",
]

samples_per_axis = 1
fake_packet = np.zeros((8, 9), dtype=int)

from buffer import Buffer
buffer = Buffer(samples_per_axis)

for i in range(6):
    input("({}/6) Place band to calibrate {}".format(i+1, calibration_messages[i]))
    for j in range(samples_per_axis):
        buffer.append(axis=j, packet=fake_packet)
        
buffer.print()

    
