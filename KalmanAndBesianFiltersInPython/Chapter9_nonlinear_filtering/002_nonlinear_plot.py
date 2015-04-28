import numpy as np
import matplotlib.pyplot as plt

data = np.random.normal(size=500000)
data2 = np.random.normal(loc=10,size=500000)

def f1(x):
    return 0.5*x

def f2(x):
    return x*x

def f3(x):
    return np.sin(x)

plt.hist(data, bins=100, color='r')
plt.hist(f3(data), bins=100, color='b')
plt.show()
