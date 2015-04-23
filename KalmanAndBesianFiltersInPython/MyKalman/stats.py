"""

Author: Roger Labbe
Modifier: Maxiee
"""

import math
import numpy as np
from scipy.stats import norm
import scipy.stats
import matplotlib.pyplot as plt
import numpy.linalg as linalg
from matplotlib.patches import Ellipse



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

def covariance_ellipse(P, deviations=1):
    """ returns a tuple defining the ellipse representing the 2 dimensional
    covariance matrix P.

    Parameters
    ----------
    P : nd.array shape (2,2)
       covariance matrix

    deviations : int (optional, default = 1)
       # of standard deviations. Default is 1.

    Returns (angle_radians, width_radius, height_radius)
    """
    U,s,v = linalg.svd(P)
    orientation = math.atan2(U[1,0],U[0,0])
    width  = deviations*math.sqrt(s[0])
    height = deviations*math.sqrt(s[1])

    assert width >= height

    return (orientation, width, height)

def plot_covariance_ellipse(
        mean,
        cov=None,           #2x2 covariance matrix
        variance=1.0,
        ellipse=None,       #(angle, width, height)
        title=None,
        axis_equal=True,
        facecolor='none',
        edgecolor='#004080',
        alpha=1.0,
        xlim=None,
        ylim=None):
    """绘制二维状态向量置信域"""

    assert cov is None or ellipse is None
    assert not (cov is None and ellipse is None)

    if cov is not None:
        ellipse = covariance_ellipse(cov)
    if axis_equal:
        plt.axis('equal')
    if title is not None:
        plt.title(title)
    if np.isscalar(variance):
        variance=[variance]
    ax = plt.gca()
    angle = np.degrees(ellipse[0])
    width = ellipse[1] * 2.
    height = ellipse[2] * 2.

    for var in variance:
        sd = np.sqrt(var)
        e = Ellipse(xy=mean, width=sd*width, height=sd*height, angle=angle,
                    facecolor=facecolor,
                    edgecolor=edgecolor,
                    alpha=alpha,
                    lw=2)
        ax.add_patch(e)
    plt.scatter(mean[0], mean[1], marker='+') # mark the center
    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)
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
