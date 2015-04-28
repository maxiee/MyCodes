import numpy as np
import scipy.misc
import matplotlib.pyplot as plt
import copy

l = scipy.misc.lena()
l_new = copy.deepcopy(l)

A = np.array([[0,1],[1,0]])

for i in range(512):
    for j in range(512):
        cor = np.array([i,j])
        cor_new = A.dot(cor)
        l_new[cor_new[0]][cor_new[1]] = l[i][j]

plt.imshow(l_new)
plt.show()
