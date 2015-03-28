import numpy.random as random
import copy
import matplotlib.pyplot as plt
from utils import book_plots as bp
from filterpy.kalman import KalmanFilter
import numpy as np



class PosSensor1(object):
    def __init__(self, pos=[0,0], vel=(0,0), noise_scale = 1.):
        self.vel = vel
        self.noise_scale = noise_scale
        self.pos = copy.deepcopy(pos)
    
    def read(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        return [self.pos[0] + random.randn() * self.noise_scale,
                self.pos[1] + random.randn() * self.noise_scale]

tracker = KalmanFilter(dim_x=4, dim_z=2)
dt = 1.
tracker.F = np.array([[1, dt, 0, 0],
                      [0,  1, 0, 0],
                      [0,  0, 1, dt],
                      [0,  0, 0, 1]])
tracker.u = 0.
tracker.H = np.array([[1/0.3084, 0, 0, 0],
                      [0, 0, 1/0.3084, 0]])
tracker.R = np.array([[5,0],
                      [0,5]])
tracker.Q = np.eye(4) * 0.1
tracker.P = np.eye(4) * 500

count = 30
xs, ys = [],[]
pxs, pys = [],[]
sensor = PosSensor1([0,0], (2,1), 1)

for i in range(count):
    pos = sensor.read()
    z = np.array([[pos[0]], [pos[1]]])
    tracker.predict()
    tracker.update(z)
    
    xs.append(tracker.x[0,0])
    ys.append(tracker.x[2,0])
    pxs.append(pos[0]*.3084)
    pys.append(pos[1]*.3084)
    
bp.plot_filter(xs, ys)
bp.plot_measurements(pxs, pys)
plt.legend(loc=2)
plt.xlim((0,20))
