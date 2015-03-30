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
    r = np.sqrt(x[0]**2 + x[2]**2)
    angle = np.arctan2(x[2],x[0])
    return np.array([r, angle])

dt = 1.0
random.seed(1234)

ukf = UnscentedKalmanFilter(dim_x=4, dim_z=2, fx=f_cv, hx=h_cv, dt=dt, kappa=0)
ukf.x = np.array([400., 0., 300., 0.])
ukf.R = np.diag([25, 1])
ukf.Q[0:2,0:2] = Q_discrete_white_noise(2, dt, var=0.02)
ukf.Q[2:4,2:4] = Q_discrete_white_noise(2, dt, var=0.02)

uxs = []
zs = []
txs = []
radius = 100
delta = 2*np.pi/360*10
for i in range(5):
    # 真实位置
    target_pos_x = 300+math.cos(i*delta)*radius + random.randn()*0.0001
    target_pos_y = 300+math.sin(i*delta)*radius + random.randn()*0.0001
    txs.append((target_pos_x, target_pos_y))
    
    # 测量位置
    zr = np.sqrt(target_pos_x**2 + target_pos_y**2) + random.randn()*5
    za = np.arctan2(target_pos_y,target_pos_x) + random.randn()*1
    zs.append([zr,za])
    
    ukf.predict()
    ukf.update(zs[-1])
    uxs.append(ukf.x.copy())
    
uxs = np.asarray(uxs)
txs = np.asarray(txs)
zs = np.asarray(zs)
plt.plot(uxs[:,0], uxs[:,2])
plt.plot(txs[:,0], txs[:,1])
#plt.plot(zs[:,.0], zs[:,1],'ro')
plt.legend(('Filter','True'), loc=4)
plt.show()
plt.plot(zs[:,0])
plt.plot(zs[:,1])
plt.show()