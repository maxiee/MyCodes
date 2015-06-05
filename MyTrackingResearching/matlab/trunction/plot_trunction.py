import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

range=np.arange(-5, 5, 0.001)
plt.plot(range, norm.pdf(range, 0, 1),'k')
plt.axvspan(-2, -1, facecolor='0.5',alpha=0.3)
plt.annotate('Constraints', xy=(-2,0.3), xycoords='data',
        xytext=(-80,10), textcoords='offset points',
        arrowprops=dict(arrowstyle="->"))
plt.scatter(-1.3, norm.pdf(-1.3, 0, 1), s=60, c='0.5')
plt.annotate('Constrained\nestimate', xy=(-1.3, norm.pdf(-1.3,0,1)),
        xycoords='data', xytext=(-100,10),textcoords='offset points',
        arrowprops=dict(arrowstyle="->"))
plt.scatter(0, norm.pdf(0, 0, 1), s=60, c='0.5')
plt.annotate('Unconstrained\nestimate', xy=(0, norm.pdf(0,0,1)),
        xycoords='data', xytext=(-100,20),textcoords='offset points',
        arrowprops=dict(arrowstyle="->"))
plt.ylim(0, 0.5)
plt.xlabel('x')
plt.ylabel('PDF(x)')
plt.show()
