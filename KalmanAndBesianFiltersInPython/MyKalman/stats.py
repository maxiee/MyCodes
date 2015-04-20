"""

Author: Roger Labbe
Modifier: Maxiee
"""

import math
import numpy as np
from scipy.stats import norm
import scipy.stats
import matplotlib.pyplot as plt

def gaussian(x, mean, var):
    """pdf of Gaussian distribution"""
    _two_pi = 2*math.pi
    return (np.exp((-0.5*(np.asarray(x)-mean)**2)/var) / 
            np.sqrt(_two_pi*var))

def multiply(mu1, var1, mu2, var2):
    if var1 == 0.0:
        var1 = 1.e-80
    if var2 == 0.0:
        var2 = 1.e-80
    mean = (var1*mu2 + var2*mu1) / (var1+var2)
    variance = 1 / (1/var1 + 1/var2)
    return (mean, variance)

def plot_gaussian(
        mean, 
        variance,
        mean_line=False,            # 在均值处化一条线 
        xlim=None,                  # x轴范围,tuple (low,high)
        xlabel=None, ylabel=None):  # 指定x、y轴label
    sigma = math.sqrt(variance)
    n = norm(mean, sigma)

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

def norm_cdf (
        x_range,        # tuple(float. float)
        mu,
        var=1,
        std=None):      # 标准差,若给出,替换var
    """ 计算高斯分布两点之间的概率　"""
    
    if std is None:
        std = math.sqrt(var)
    return abs(norm.cdf(x_range[0], loc=mu, scale=std) - 
               norm.cdf(x_range[1], loc=mu, scale=std))

if __name__ == "__main__":

    # 高斯相乘实验

    xs = np.arange(0, 60, 0.1)

    mean1, var1 = 10, 5
    mean2, var2 = 50, 5

    mean, var = multiply(mean1, var1, mean2, var2)

    ys = [gaussian(x, mean1, var1) for x in xs]
    plt.plot(xs, ys, label='measure 1')

    ys = [gaussian(x, mean2, var2) for x in xs]
    plt.plot(xs, ys, label='measure 2')
 
    ys = [gaussian(x, mean, var) for x in xs]
    plt.plot(xs, ys, label='result')

    plt.legend(loc='best')
    plt.show()
