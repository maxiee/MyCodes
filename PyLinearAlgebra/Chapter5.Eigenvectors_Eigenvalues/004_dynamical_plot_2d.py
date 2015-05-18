import matplotlib.pyplot as plt
import numpy as np

A = np.array([
        [.5, -.6],
        [.75, 1.1]])

init = np.array([2, 0]).T

xs = [init[0]]
ys = [init[1]]

for i in range(10):
    init = A.dot(init)
    xs.append(init[0])
    ys.append(init[1])

plt.plot(xs, ys, '--o')
plt.show()
