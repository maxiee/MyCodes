import numpy.random as random
import matplotlib.pyplot as plt


def volt(voltage, temp_variance):
    return random.randn()*temp_variance + voltage

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

movement = 0  
variance = 2.13 ** 2
movement_variance = 0.2
actual_voltage = 16.3

N = 50
zs = [volt(actual_voltage, variance) for i in range(N)]
ps = []
estimates = []

kf = KalmanFilter1D(x0=25,
                    P=1000,
                    R=variance,
                    Q=movement_variance)

for i in range(N):
    kf.predict(movement)
    kf.update(zs[i])
    estimates.append(kf.x)
    ps.append(kf.P)

plt.plot(zs)
plt.plot(estimates)
plt.legend(("M","F"), loc="best")
plt.show()
plt.plot(ps)
plt.show()
print ps[-1]