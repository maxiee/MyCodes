import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy.random as random
import math

class OneDSensor(object):
    def __init__(self,
            x0=0,   # 初始位置
            velocity=1,
            measurement_variance=0.0,
            process_variance=0.0):
        self.x = x0
        self.velocity = velocity
        self.noise = math.sqrt(measurement_variance)
        self.pnoise = math.sqrt(process_variance)
        self.constant_vel = velocity

    def sense_position(self):
        # random.rand() 0-1均匀分布
        # random.randn() 均值为0的正态分布
        pnoise = abs(random.rand() * self.pnoise)
        if self.velocity > self.constant_vel:
            pnoise = -pnoise
        self.velocity += pnoise
        self.x = self.x + self.velocity
        return self.x + random.randn() * self.noise

if __name__ == "__main__":

    count = 100
    dog = OneDSensor(measurement_variance=4.0)
    xs = []
    dog2 = OneDSensor(measurement_variance=100.0)
    xs2 = []
    dog3 = OneDSensor(process_variance=0.5)
    xs3 = []
    xs_real = [i for i in range(count)]
    for i in range(count):
        x = dog.sense_position()
        xs.append(x)

        x2 = dog2.sense_position()
        xs2.append(x2)

        x3 = dog3.sense_position()
        xs3.append(x3)

    plt.plot(xs_real, label='real', lw=2)
    plt.plot(xs, label='Sensor')
    plt.plot(xs2, label='Sensor2')
    plt.plot(xs3, label='Sensor3')
    plt.legend(loc='best')
    plt.show()
