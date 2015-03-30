from numpy.random import randn
import numpy as np
from numpy import sin, cos, tan, log
import matplotlib.pyplot as plt

from numpy.random import multivariate_normal

def f(x,y):
    return x+y, .1*x**2 +y*y
    
mean = (0,0)
p = np.array([[32, 15],[15., 40.]])

xs, ys = multivariate_normal(mean=mean, cov=p, size=50000).T
fxs, fys = [],[]
for x,y in zip(xs, ys):
    fx, fy = f(x,y)
    
    fxs.append(fx)
    fys.append(fy)

mean_fx = f(*mean)

computed_mean_x = np.average(fxs)
computed_mean_y = np.average(fys)

plt.subplot(121)
plt.scatter(xs, ys, marker='.', alpha=0.01)
plt.axis('equal')

plt.subplot(122)
plt.scatter(fxs, fys, marker='.', alpha=0.01)
plt.scatter(mean_fx[0], mean_fx[1],
            marker='v', s=300, c='k', label='Linearized Mean')
plt.scatter(computed_mean_x, computed_mean_y,
            marker='*', s=120, c='r', label='Computed Mean')
plt.ylim([-10, 290])
plt.xlim([-150, 150])
plt.legend(loc='best', scatterpoints=1)
plt.show()
print "Difference in mean"
print "x = %.3f" % (computed_mean_x-mean_fx[0])
print "y = %.3f" % (computed_mean_y-mean_fx[1])