import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg as LA

def inner_product(u, v):
    len_u = len(u)
    len_v = len(v)
    if len_u != len_v:
        return None
    ret = 0
    for i in range(len_u):
        ret += u[i] * v[i]
    return ret

def project(y, u):
    return inner_product(y, u)/inner_product(u, u)*u

A = np.array([[4,0],[0,2],[1,1]])

b = np.array([2,0,11]).T

Q, R = LA.qr(A)

print("求解公式:", LA.inv(A.T.dot(A)).dot(A.T).dot(b))

print("投影法:", project(b, Q[:,0])+project(b, Q[:,1]))

