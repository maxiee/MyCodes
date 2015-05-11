import statutils
import numpy as np
import matplotlib.pyplot as plt

def plot_3d_cov():
    mean = (2,17)
    cov = np.array([[10, 0], [0, 4]])
    statutils.plot_3d_covariance(mean, cov)
    plt.show()

plot_3d_cov()

