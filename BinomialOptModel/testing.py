import numpy as np
import math

matrix = np.zeros([5,5])

for i in range(5):
    for j in range(5):
        matrix [i,j] = 10*i+j

print(matrix)
print(matrix[:,1])

array = np.arange(5,-1,-1)
print(array)
