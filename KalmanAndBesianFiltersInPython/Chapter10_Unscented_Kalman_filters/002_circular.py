# -*- coding: utf-8 -*-
import math
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.common import Q_discrete_white_noise
from numpy import random
import numpy as np
from matplotlib import pyplot as plt

def f_cv(x, dt):
    F = np.array([[1, dt, 0, 0],
                  [0,  1, 0, 0],
                  [0,  0, 1, dt],
                  [0,  0, 0, 1]])
    return np.dot(F, x)

def h_cv(x):
    return np.array([x[0], x[2]])

dt = 1.0
random.seed(1234)

ukf = UnscentedKalmanFilter(dim_x=4, dim_z=2, fx=f_cv, hx=h_cv, dt=dt, kappa=0)
ukf.x = np.array([100., 0., 0., 0.])
ukf.R = np.diag([25, 25])
ukf.Q[0:2,0:2] = Q_discrete_white_noise(2, dt, var=0.02)
ukf.Q[2:4,2:4] = Q_discrete_white_noise(2, dt, var=0.02)

uxs = []
zs = []
txs = []
radius = 100
delta = 2*np.pi/360*10
for i in range(34):
    # 真实位置
    target_pos_x = math.cos(i*delta)*radius + random.randn()*0.0001
    target_pos_y = math.sin(i*delta)*radius + random.randn()*0.0001
    txs.append((target_pos_x, target_pos_y))
    
    # 测量位置
    zx = target_pos_x + random.randn()*5
    zy = target_pos_y + random.randn()*5
    zs.append((zx,zy))
    
    ukf.predict()
    ukf.update(np.array([zx, zy]))
    uxs.append(ukf.x.copy())
    
uxs = np.asarray(uxs)
txs = np.asarray(txs)
zs = np.asarray(zs)
plt.plot(uxs[:,0], uxs[:,2])
plt.plot(txs[:,0], txs[:,1])
plt.plot(zs[:,.0], zs[:,1],'ro')
plt.legend(('Filter','True','Measurement'), loc=4)
plt.show()