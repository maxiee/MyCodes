from matplotlib.patches import Ellipse 
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg
import math
import scipy.stats as stats
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def covariance_ellipse(P, deviations=1):
    U,s,v = linalg.svd(P)
    orientation = math.atan2(U[1,0],U[0,0])
    width  = math.sqrt(s[0])*deviations
    height = math.sqrt(s[1])*deviations
    return (orientation, width, height)

def plot_covariance_ellipse(mean, cov=None):
    """ plots the covariance ellipse where
    mean is a (x,y) tuple for the mean of the covariance (center of ellipse)
    cov is a 2x2 covariance matrix.
    """    
    ellipse = covariance_ellipse(cov)
    plt.axis('equal')
    ax = plt.gca()

    angle = np.degrees(ellipse[0])
    width = ellipse[1] * 2.
    height = ellipse[2] * 2.

    e = Ellipse(
            xy=mean, width=width, height=height, 
            angle=angle, facecolor='g', alpha=0.2)
    ax.add_patch(e)
    plt.scatter(mean[0], mean[1], marker='+') # mark the center

def plot_3d_covariance(mean, cov):
    o,w,h = covariance_ellipse(cov,3)
    # rotate width and height to x,y axis
    wx = abs(w*np.cos(o) + h*np.sin(o))*1.2
    wy = abs(h*np.cos(o) - w*np.sin(o))*1.2
    # scale w 拿来重用
    if wx > wy:
        w = wx
    else:
        w = wy

    minx = mean[0] - w
    maxx = mean[0] + w
    miny = mean[1] - w
    maxy = mean[1] + w

    xs = np.arange(minx, maxx, (maxx-minx)/40.)
    ys = np.arange(miny, maxy, (maxy-miny)/40.)
    xv, yv = np.meshgrid (xs, ys)

    zs = np.array([100.* stats.multivariate_normal.pdf(np.array([x,y]),mean,cov) \
                   for x,y in zip(np.ravel(xv), np.ravel(yv))])
    zv = zs.reshape(xv.shape)

    ax = plt.figure().add_subplot(111, projection='3d')
    ax.plot_surface(xv, yv, zv, rstride=1, cstride=1, cmap=cm.autumn)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    ax.contour(xv, yv, zv, zdir='x', offset=minx-1, cmap=cm.autumn)
    ax.contour(xv, yv, zv, zdir='y', offset=maxy, cmap=cm.BuGn)
