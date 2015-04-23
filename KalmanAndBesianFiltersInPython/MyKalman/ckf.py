# -*- coding: utf-8 -*-
import numpy as np
from numpy import asarray, eye, zeros, dot, isscalar, outer
from numpy.linalg import inv, cholesky
from filterpy.common import dot3


class CubatureKalmanFilter(object):
    
    def __init__(
            self, 
            dim_x,    # int, number of state variables 
            dim_z,    # int, number of measurement inputs 
            dt,       # float, time step 
            hx,       # measurement function 
            fx):      # state transformed function
        
        self.Q = eye(dim_x)
        self.R = eye(dim_z)
        self.x = zeros(dim_x)
        self.P = eye(dim_x)
        self._dim_x = dim_x
        self._dim_z = dim_z
        self._dt = dt
        self._num_cubatures = 2*dim_x
        self.hx = hx
        self.fx = fx

        # Kalman Gain
        self.K = 0

        # weights for cubature points
        self.W = np.zeros(2*dim_x) + 1./(2*dim_x) 
        # cubature points
        self.cubatures_f = zeros((self._num_cubatures, self._dim_x))
    
    def update(
            self, 
            z,                      # measurement vector
            R=None,                 # measurement noise 
            residual=np.subtract):  

        if isscalar(z):
            dim_z = 1
        else:
            dim_z = len(z)
        
        if R is None:
            R = self.R
        elif np.isscalar(R):
            R = eye(self._dim_z) * R
        
        cubatures_f = self.cubatures_f
        cubatures_h = zeros((self._num_cubatures,dim_z))
        
        CT = cubature_transform
        
        # transform cubature points into measurement space
        for i in range(self._num_cubatures):
            cubatures_h[i] = self.hx(cubatures_f[i])
        
        # mean and covariance of prediction
        zp, Pz = CT(cubatures_h, self.W, self.W, R)
        
        # cross variance of the state and the measurements
        self.Pxz = zeros((self._dim_x,dim_z))
        
        for i in range(self._num_cubatures):
            self.Pxz += self.W[i] * 
                np.outer(
                        cubatures_f[i] - 
                        self.x,residual(cubatures_h[i],zp))
        
        self.K = dot(self.Pxz, inv(Pz)) # Kalman gain
        y = residual(z, zp)
        
        self.x = self.x + dot(self.K, y)
        self.P = self.P - dot3(self.K, Pz, self.K.T)
    
    def predict(self, dt=None):

        if dt is None:
            dt = self._dt

        # calculate cubature points for given mean and covariance
        cubatures = self.cubature_points(self.x, self.P)
                
        for i in range(self._num_cubatures):
            self.cubatures_f[i] = self.fx(cubatures[i], dt)
        
        self.x, self.P = cubature_transform(
                            self.cubatures_f, self.W, self.W, self.Q)
    
    @staticmethod
    def cubature_points(x,P):

        if np.isscalar(x):
            x = asarray([x])
        n = np.size(x)
        
        if np.isscalar(P):
            P = eye(n)*P
        
        cubatures = zeros((2*n, n))
        
        U = cholesky(n*P).T
        
        cubatures[0:n,0:n] = eye(n)
        cubatures[n:2*n,0:n] = -1 * eye(n)
        
        for i in range(2*n):
            cubatures[i] = x + dot(U,cubatures[i])
        print "容积点最终"
        print cubatures
        return cubatures
        
def cubature_transform(Cubatures, Wm, Wc, noise_cov):
    
    kmax,n = Cubatures.shape
    
    x = dot(Wm, Cubatures)
    
    P = zeros((n,n))
    for k in range(kmax):
        y = Cubatures[k] - x
        P += np.outer(y,y) * Wc[k]
    
    if noise_cov is not None:
        P += noise_cov
    
    return (x,P)
    
    
