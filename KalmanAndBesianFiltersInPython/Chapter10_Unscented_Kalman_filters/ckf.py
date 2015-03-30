# -*- coding: utf-8 -*-
import numpy as np
from numpy import asarray, eye, zeros, dot, isscalar, outer
from numpy.linalg import inv, cholesky


class CubatureKalmanFilter(object):
    
    def __init__(self, dim_x, dim_z, dt, hx, fx):
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
        self.W = np.zeros((dim_x,1))*1./(2*dim_x)
        # cubature points
        self.cubatures_f = zeros((self._num_cubatures, self._dim_x))
    
    def update(self, z, R=None, residual=np.subtract):
        if isscalar(z):
            dim_z = 1
        else:
            dim_z = len(z)
        
        if R is None:
            R = self.R
        else:
            R = eye(self._dim_z) * R
        
        cubatures_f = self.cubatures_f
        cubatures_h = zeros((self._num_cubatures, dim_z))
        
        CT = cubature_transform
        
        for i in range(self._num_cubatures):
            cubatures_h[i] = self.hx(cubatures_f[i])
        
        # mean and covariance of prediction
        zp, Pz = CT(cubatures_h, self.W, self.W, R)
        
        # cross variance of the state and the measurements
        self.Pxz = zeros((self._dim_x, dim_z))
        for i in range(self._num_cubatures):
            self.Pxz += self.W[i]*np.outer(cubatures_f[i]-self.x,residual(cubatures_h[i],zp))
        
        self.K = dot(self.Pxz, inv(Pz))
        y = residual(z, zp)
        
        self.x = self.x + dot(self.K, y)
        self.P = self.P - dot(self.K, Pz).dot(self.K.T)
    
    def predict(self, dt=None):
        if dt is None:
            dt = self._dt
        # calculate cubature points for given mean and covariance
        cubatures = self.cubature_points(self.x, self.P)
        
        print cubatures[:,0]
        
        for i in range(self._num_cubatures):
            self.cubatures_f[i] = self.fx(cubatures[:,i], dt).T
        
        self.x, self.P = cubature_transform(
                            self.cubatures_f, self.W, self.W, self.Q)
    
    @staticmethod
    def cubature_points(x,P):
        if np.isscalar(x):
            x = asarray([x])
        n = np.size(x)
        print n
        
        if np.isscalar(P):
            P = eye(n)*P
        
        cubatures = zeros((n, 2*n))
#        print cubatures
        
        U = cholesky(P).T
        
        cubatures[0:n,0:n] = eye(n)
        cubatures[0:n,n:2*n] = -1 * eye(n)
        cubatures *= np.sqrt(n)
        
        for i in range(2*n):
            cubatures[:,i] = dot(U,cubatures[:,i])
        return cubatures
        
def cubature_transform(Cubatures, Wm, Wc, noise_cov):
    
    kmax, n = Cubatures.shape
    
    print Wm
    print Cubatures
    
    x = dot(Wm, Cubatures)
    
    P = zeros((n,n))
    for k in range(kmax):
        y = Cubatures[k] - x
        P += Wc[k] + np.outer(y,y)
    
    if noise_cov is not None:
        P += noise_cov
    
    return (x,P)
    
    