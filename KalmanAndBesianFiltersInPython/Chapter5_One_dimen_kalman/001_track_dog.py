import matplotlib.pyplot as plt
import numpy.random as random
import math
import numpy as np
import scipy.stats as stats

class KalmanFilter1D:
    def __init__(self, x0, P, R, Q):
        self.x = x0 # esimated value of the filter
        self.P = P  # variance of the state
        self.R = R  # measurement error
        self.Q = Q  # movement error
    
    def update(self, z): # just multiply
        self.x = (self.P*z + self.x*self.R) / (self.P + self.R)
        self.P = 1. / (1./self.P + 1./self.R)
    
    def predict(self, u=0.0): # jsut predict
        self.x += u
        self.P += self.Q


def multiply(mu1, var1, mu2, var2):
    if var1 == 0:
        var1 = 1e-80
    
    if var2 == 0:
        var2 = 1e-80
    mean = (var1*mu2 + var2*mu1) / (var1+var2)
    variance = 1 / (1/var1 + 1/var2)
    return (mean, variance)

def update(mean, variance, measurement, measurement_variance):
    return multiply(mean, variance, measurement, measurement_variance)

def predict(pos, variance, movement, movement_variance):
    return (pos + movement, variance + movement_variance)

class DogSensor(object):
    
    def __init__(self, x0=0, velocity=1,
                 measurement_variance=0.0,
                 process_variance=0.0):
        
        self.x = x0
        self.velocity = velocity
        self.noise = math.sqrt(measurement_variance)
        self.pnoise = math.sqrt(process_variance)
        self.constant_vel = velocity
    
    def sense_position(self):
        pnoise = abs(random.rand()*self.pnoise)
        if self.velocity > self.constant_vel:
            pnoise = -pnoise
        self.velocity += pnoise
        self.x = self.x + self.velocity
        return self.x + random.randn()*self.noise


movement = 1
movement_variance = 2.0
sensor_variance = 4.5
pos = (0, 100)

dog = DogSensor(pos[0],
                velocity=movement,
                measurement_variance=sensor_variance,
                process_variance=sensor_variance)

zs = []
ps = []

for i in range(50):
    pos = predict(pos[0], pos[1], movement, movement_variance)
    print "PRE:{: 10.4f} {: 10.4f}".format(pos[0],pos[1]) ,
    
    z = dog.sense_position()
    zs.append(z)
    
    pos = update(pos[0], pos[1], z, sensor_variance)
    ps.append(pos[0])
    print "UPD:{: 10.4f} {: 10.4f}".format(pos[0],pos[1])

plt.plot(ps)
plt.plot(zs)
plt.legend(["filter", "measurement"], loc="best")
plt.show()
