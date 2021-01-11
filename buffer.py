import numpy as np

class Buffer:
    def __init__(self, samples_per_axis) -> None:
        super().__init__()                      

        self.buffer = np.ndarray((6, samples_per_axis, 8, 9), dtype=int)
        self.head = 0
        self.samples_per_axis = samples_per_axis
        self.axis = 0

    def append(self, packet) -> bool:
        self.buffer[self.axis][self.head] = packet
        self.head+=1
        if self.filled():
            self.head = 0
            self.axis+=1

    def filled(self):
        return False if self.head < self.samples_per_axis else True     
    
    def print(self):
        print(self.buffer)