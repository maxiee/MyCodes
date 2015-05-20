import matplotlib.pyplot as plt
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

y = np.array([7, 6]).T
u = np.array([4, 2]).T

r = project(y, u)

print(r)

#plot result
plt.figure()
plt.plot([0, y[0]], [0, y[1]],lw=2, label='y')
plt.plot([0, u[0]], [0, u[1]],lw=2, label='u')
plt.plot([0, r[0]], [0, r[1]],'--', label='r')
plt.arrow(
    y[0], y[1], (r[0]-y[0])*.95, (r[1]-y[1])*.95,
    linestyle='dashed', alpha=0.2)
plt.legend(loc='best')
plt.show()


