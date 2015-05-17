import numpy as np
from numpy import linalg as LA

A = np.array([
        [.95, .03],
        [.05, .97]])

w,v = LA.eig(A)

print("特征值:\n", w)
print("特征矢量:\n", v)
