import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

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

u1 = np.array([2, 5, -1]).T
u2 = np.array([-2, 1, 1]).T
y = np.array([1, 2, 3]).T

p1 = project(y, u1)
p2 = project(y, u2)
p = p1 + p2

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot([0,u1[0]], [0,u1[1]], [0,u1[2]])
ax.plot([0,u2[0]], [0,u2[1]], [0,u2[2]])
ax.scatter(0, 0, 0)
ax.scatter(y[0], y[1], y[2], color='r')
ax.scatter(p[0], p[1], p[2], color='r')
ax.scatter(p1[0], p1[1], p1[2])
ax.scatter(p2[0], p2[1], p2[2])
ax.plot([y[0], p[0]], [y[1], p[1]], [y[2], p[2]], '--')
ax.plot([y[0], p1[0]], [y[1], p1[1]], [y[2], p1[2]], '--', color='g', alpha=0.5)
ax.plot([y[0], p2[0]], [y[1], p2[1]], [y[2], p2[2]], '--', color='g', alpha=0.5)
ax.plot([p[0], p1[0]], [p[1], p1[1]], [p[2], p1[2]], '--', color='g', alpha=0.5)
ax.plot([p[0], p2[0]], [p[1], p2[1]], [p[2], p2[2]], '--', color='g', alpha=0.5)
plt.show()
