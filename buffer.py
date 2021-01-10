import numpy as np

class Buffer:
    def __init__(self, samples_per_axis) -> None:
        super().__init__()                      

        self.buffer = np.ndarray((6, samples_per_axis, 8, 9), dtype=int)
        self.head = 0
        self.samples_per_axis = samples_per_axis

    def append(self, axis, packet) -> bool:
        if self.filled(): 
            self.head = 0
            return False
        else:
            self.buffer[axis][self.head] = packet
            self.head+=1
            return True

    def filled(self):
        return True if self.head >= self.samples_per_axis else False     
    
    def print(self):
        print(self.buffer)