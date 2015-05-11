from matplotlib.patches import Ellipse 
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as linalg
import math

def covariance_ellipse(P):
    U,s,v = linalg.svd(P)
    orientation = math.atan2(U[1,0],U[0,0])
    width  = math.sqrt(s[0])
    height = math.sqrt(s[1])
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

P = np.array([[2,0],[0,4]])
plot_covariance_ellipse((0,0), P)
P2 = np.array([[6,2.5],[2.5,.6]])
plot_covariance_ellipse((10,2), P2)

plt.show()
