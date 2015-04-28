import numpy as np
import matplotlib.pyplot as plt

A = np.array([[1,3],[3,1]])

x0 = np.array([0, 10])
x1 = np.array([8, 0])
x2 = np.array([2, -2])
x3 = np.array([5, 5])

def linear_trans(x):
    plt.scatter(x[0], x[1], color='r')
    x_trans = A.dot(x)
    plt.scatter(x_trans[0], x_trans[1], color='b')
    plt.arrow(x[0],x[1],(x_trans[0]-x[0])*0.95,(x_trans[1]-x[1])*0.95, head_width=0.5, linestyle='dashed', alpha=0.2)
    print(x),
    print(x_trans)

linear_trans(x0)
linear_trans(x1)
linear_trans(x2)
linear_trans(x3)

plt.show()

