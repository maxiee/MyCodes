# -*- coding: utf-8 -*-
import math
from filterpy.kalman import UnscentedKalmanFilter
from filterpy.common import Q_discrete_white_noise
from numpy import random
import numpy as np
from matplotlib import pyplot as plt
from ckf import CubatureKalmanFilter

def f_cv(x, dt):
    F = np.array([[1, dt, 0, 0],
                  [0,  1, 0, 0],
                  [0,  0, 1, dt],
                  [0,  0, 0, 1]])
    return np.dot(F, x)

def h_cv(x):
    return np.array([x[0], x[2]])

def e(x):
    res = []
    for n in range(x.shape[0]):
        res.append(np.sqrt(x[n][0]**2+x[n][2]**2))
    return res

dt = 1.0
random.seed(1234)

ukf = UnscentedKalmanFilter(dim_x=4, dim_z=2, fx=f_cv, hx=h_cv, dt=dt, kappa=0)
ukf.x = np.array([100., 0., 0., 0.])
ukf.R = np.diag([25, 25])
ukf.Q[0:2,0:2] = Q_discrete_white_noise(2, dt, var=0.04)
ukf.Q[2:4,2:4] = Q_discrete_white_noise(2, dt, var=0.04)

ckf = CubatureKalmanFilter(dim_x=4, dim_z=2, fx=f_cv, hx=h_cv, dt=dt)
ckf.x = np.array([100., 0., 0., 0.])
ckf.R = np.diag([25, 25])
ckf.Q[0:2,0:2] = Q_discrete_white_noise(2, dt, var=0.04)
ckf.Q[2:4,2:4] = Q_discrete_white_noise(2, dt, var=0.04)

uxs = []
pxs = []
zs = []
txs = []
cxs = []
radius = 100
delta = 2*np.pi/360*5
for i in range(70):
    # 真实位置
    target_pos_x = math.cos(i*delta)*radius + random.randn()*0.00
    target_pos_y = math.sin(i*delta)*radius + random.randn()*0.0001
    txs.append((target_pos_x, target_pos_y))
    
    # 测量位置
    zx = target_pos_x + random.randn()*5
    zy = target_pos_y + random.randn()*5
    zs.append([zx,zy])
    
    ukf.predict()
    ukf.update([zx,zy])
    
    ckf.predict()
    ckf.update([zx,zy])
    cxs.append(ckf.x)
    
    #pukf
    pSigma = e(ukf.sigmas_f)
    dHat = np.sum(pSigma)/len(pSigma)
    pddPukf = 0
    pxdPukf = np.zeros((1,4))
#    print ukf.x
#    print pSigma[0]
#    print ukf.sigmas_f[0]
    for i in range(len(pSigma)):
        pddPukf += ukf.W[i]*(
            (pSigma[i] - dHat)*(pSigma[i] - dHat))
        pxdPukf += ukf.W[i]*(
            (ukf.sigmas_f[i]-ukf.x)*(pSigma[i]-dHat))
    pKalman = pxdPukf / pddPukf
#    print pKalman
#    print dHat
#    print pSigma
    
    #pukf2
#    print ukf.K
    pukf = ukf.x + pKalman*(radius-dHat)
#    print pukf
    pxs.append(pukf[0].copy())
    uxs.append(ukf.x.copy())
    
uxs = np.asarray(uxs)
txs = np.asarray(txs)
pxs = np.asarray(pxs)
cxs = np.asarray(cxs)
zs = np.asarray(zs)
plt.plot(uxs[:,0], uxs[:,2],'--')
plt.plot(txs[:,0], txs[:,1],':')
plt.plot(pxs[:,0], pxs[:,2],'-')
plt.plot(cxs[:,0], cxs[:,2],'-o')
#plt.plot(zs[:,.0], zs[:,1],'ro')
plt.legend(('Filter','True','PUKF'), loc=4)
plt.show()
#plt.plot(zs[:,0])
#plt.plot(zs[:,1])
#plt.show()