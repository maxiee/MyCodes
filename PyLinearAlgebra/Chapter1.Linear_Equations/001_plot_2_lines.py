import numpy as np
import matplotlib.pyplot as plt

A = np.array([[1, -2],[-1, 3]])

b = np.array([-1,3])

print(np.linalg.solve(A, b))

x = np.arange(-10, 10)
print(x)

for i in range(A.shape[0]):
    y = (b[i] - A[i][0]*x) / A[i][1]
    plt.plot(x, y)
solution = np.linalg.solve(A,b)
plt.scatter(solution[0], solution[1])
plt.show()

    
