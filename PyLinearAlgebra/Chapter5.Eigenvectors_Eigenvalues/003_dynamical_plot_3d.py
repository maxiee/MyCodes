import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import numpy as np

A = np.array([
    [0,   0, .33],
    [.18, 0, 0  ],
    [0, .71, .94]])

MAX = 1000
x0 = np.array([MAX, 0, 0]).T
x1 = np.array([0, MAX, 0]).T
x2 = np.array([0, 0, MAX]).T

points = [x0, x1, x2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

labels = ["juvenile only", "subadult only", "adult only"]
for i in range(len(points)):
    point = points[i]
    x = [point[0]]
    y = [point[1]]
    z = [point[2]]
    for j in range(100):
        point = A.dot(point)
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.plot(x, y, z, '-o', label = labels[i])
ax.legend()
ax.set_xlabel("juvenile")
ax.set_ylabel("subadult")
ax.set_zlabel("adult")
plt.show()
