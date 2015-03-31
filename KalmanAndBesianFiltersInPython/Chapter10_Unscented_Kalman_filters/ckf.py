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
        self.W = np.zeros((1,2*dim_x))+1./(2*dim_x)
        # cubature points
        self.cubatures_f = zeros((self._dim_x, self._num_cubatures))
    
    def update(self, z, R=None, residual=np.subtract):
        if isscalar(z):
            dim_z = 1
        else:
            dim_z = len(z)
        
        if R is None:
            R = self.R
        elif np.isscalar(R):
            R = eye(self._dim_z) * R
        
        cubatures_f = self.cubatures_f
        cubatures_h = zeros((dim_z,self._num_cubatures))
        
        CT = cubature_transform
        
        # transform cubature points to measurement space
        for i in range(self._num_cubatures):
            cubatures_h[:,i] = self.hx(cubatures_f[:,i])
#        print "观测容积点"
#        print cubatures_h
        
        # mean and covariance of prediction
        zp, Pz = CT(cubatures_h, self.W, self.W, R)
        
        # cross variance of the state and the measurements
        self.Pxz = zeros((self._dim_x,dim_z))
        
        for i in range(self._num_cubatures):
            self.Pxz += self.W[0,i]*np.outer(cubatures_f[:,i]-self.x,residual(cubatures_h[:,i],zp))
        
        self.K = dot(self.Pxz, inv(Pz))
        y = residual(z, zp)
        
#        print "K"
#        print self.K
#        print y
#        print self.x.shape
#        print self.K.shape
#        print y.shape
        self.x = self.x + dot(self.K, y.T).T
        self.P = self.P - dot(self.K, Pz).dot(self.K.T)
    
    def predict(self, dt=None):
        if dt is None:
            dt = self._dt
        # calculate cubature points for given mean and covariance
        cubatures = self.cubature_points(self.x, self.P)
                
        for i in range(self._num_cubatures):
            self.cubatures_f[:,i] = self.fx(cubatures[:,i], dt)
        
        print "变换后的容积点"
        print self.cubatures_f
        
        self.x, self.P = cubature_transform(
                            self.cubatures_f, self.W, self.W, self.Q)
        print "预测步骤结果：",self.x,self.P

    
    @staticmethod
    def cubature_points(x,P):

        if np.isscalar(x):
            x = asarray([x])
        n = np.size(x)
        
        if np.isscalar(P):
            P = eye(n)*P
        
        cubatures = zeros((n, 2*n))
        
        U = cholesky(P).T
        
        cubatures[0:n,0:n] = eye(n)
        cubatures[0:n,n:2*n] = -1 * eye(n)

        cubatures *= np.sqrt(n)
        
        for i in range(2*n):
            cubatures[:,i] = x + dot(U,cubatures[:,i])
        print "容积点最终"
        print cubatures
        return cubatures
        
def cubature_transform(Cubatures, Wm, Wc, noise_cov):
    
    n,kmax = Cubatures.shape
    
    print "x测试"
    x = dot(Wm, Cubatures.T)
    print x

    x2 = np.zeros((1,n))
    for i in range(kmax):
        x2 += Cubatures[:,i]*Wm[0,i]
    x2 /= kmax
    print x2
    
    P = zeros((n,n))
    for k in range(kmax):
        y = Cubatures[:,k] - x
        P += np.outer(y,y) * Wc[0,k]
    
    if noise_cov is not None:
        P += noise_cov
    
    return (x,P)
    
    