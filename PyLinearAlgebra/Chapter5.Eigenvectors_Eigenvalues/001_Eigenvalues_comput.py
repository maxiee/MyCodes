import numpy as np
from numpy import linalg as LA

A = np.array([
        [4, -1, 6],
        [2,  1, 6],
        [2, -1, 8]])

w,v = LA.eig(A)

print("特征值:\n", w)
print("特征矢量:\n", v)
