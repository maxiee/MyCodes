import matplotlib.pyplot as plt
import numpy.random as random
import math

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

for i in range(20):
    print '{: 5.4f}'.format(random.randn())
    if (i+1) % 5 == 0:
        print ""