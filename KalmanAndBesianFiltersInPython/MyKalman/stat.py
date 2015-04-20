"""

Author: Roger Labbe
Modifier: Maxiee
"""

import math
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def plot_gaussian(
        mean, 
        variance,
        mean_line=False,            # 在均值处化一条线 
        xlim=None,                  # x轴范围,tuple (low,high)
        xlabel=None, ylabel=None):  # 指定x、y轴label
    sigma = math.sqrt(variance)
    n = scipy.stats.norm(mean, sigma)

    if xlim is None:
        min_x = n.ppf(0.001)    # Percent point function
        max_x = n.ppf(0.999)    # 从左到右，%几的横坐标？
    else:
        min_x = xlim[0]
        max_x = xlim[1]
    xs = np.arange(min_x, max_x, (max_x-min_x)/1000)
    plt.plot(xs, n.pdf(xs))     # pdf:在此点处的pdf
    plt.xlim((min_x, max_x))

    if mean_line:
        plt.axvline(mean)       # 画一条与x轴垂直线
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.show()
