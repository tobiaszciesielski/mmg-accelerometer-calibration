import json
import numpy as np

def find_zero(a, b):
    return (a + b) / 2 

def count_k(a, b):
    return (b - a) / 2

data = np.load("numpy.npy")
extreme_values = np.mean(data[:,:,:,0:3],axis=1)
Xmin = extreme_values[0,:,0]
Xmax = extreme_values[1,:,0]
Ymin = extreme_values[2,:,1]
Ymax = extreme_values[3,:,1]
Zmin = extreme_values[4,:,2]
Zmax = extreme_values[5,:,2]

X_zero = find_zero(Xmin, Xmax)
X_k = count_k(Xmin, Xmax)

Y_zero = find_zero(Ymin, Ymax)
Y_k = count_k(Ymin, Ymax)

Z_zero = find_zero(Zmin, Zmax)
Z_k = count_k(Zmin, Zmax)

dict_to_json = {
    "X_zero":np.round(X_zero).tolist(),
    "Y_k":np.round(Y_k).tolist(),
    "Y_zero":np.round(Y_zero).tolist(),
    "X_k":np.round(X_k).tolist(),
    "Z_zero":np.round(Z_zero).tolist(),
    "Z_k":np.round(Z_k).tolist(),
}

for key, value in dict_to_json.items():
    print(key, '\t', value)

# print(json.dumps(dict_to_json))