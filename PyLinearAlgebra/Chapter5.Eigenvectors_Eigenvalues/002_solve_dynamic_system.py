import numpy as np
from numpy import linalg as LA

A = np.array([
    [0,   0, .33],
    [.18, 0, 0  ],
    [0, .71, .94]])

w,v = LA.eig(A)

for i in range(w.size):
    print("特征值:", w[i])
    print("前10步解:")
    temp = v[:, i].T
    for j in range(10):
        temp = w[i] * temp
        print("\t%d: " % j, temp)
