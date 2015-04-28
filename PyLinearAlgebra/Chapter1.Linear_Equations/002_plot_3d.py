import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

A = np.array([[1, -2, 1],[0, 2, -8],[-4, 5, 9]])
b = np.array([0, 8, -9])

x, y  = np.meshgrid(range(50), range(50))

plt3d = plt.figure().gca(projection='3d')

# 画出解
solution = np.linalg.solve(A,b)
print(solution)
plt3d.scatter(solution[0], solution[1], solution[2], s=100)

# 画出三个平面
colors = ['r', 'g', 'b']
for i in range(A.shape[0]):
    z = (-A[i][0]*x - A[i][1]*y - b[i]) / A[i][2]
    plt3d.plot_surface(x, y, z, cstride=5, rstride=5, color=colors[i], alpha=0.2)
plt.show()
