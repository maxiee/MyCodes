import numpy as np
from numpy import linalg as LA

x0 = np.array([1000, 1000, 1000]).T

A = np.array([
    [0,   0, .33],
    [.18, 0, 0  ],
    [0, .71, .94]])

w,v = LA.eig(A)

print("特征值:",w)
print("特征向量:",v)
# c = LA.inv(v).dot(x0)
