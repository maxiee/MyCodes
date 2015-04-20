import stats
import sensor
import matplotlib.pyplot as plt


def update(mean, variance, measurement, measurement_variance):
    return stats.multiply(mean, variance, measurement, measurement_variance)

def predict(pos, variance, movement, movement_variance):
    return (pos + movement, variance + movement_variance)


movement = 1
movement_variance = 2
sensor_variance = 4.5 
pos = (0, 100)

zs = []
ps = []
vs = []

dog = sensor.OneDSensor(
        pos[0],
        velocity=movement, 
        measurement_variance=sensor_variance, 
        process_variance=0.5)

for i in range(50):
    pos = predict(pos[0], pos[1], movement, movement_variance)
    print('PREDICT: {: 10.4f} {: 10.4f}' .format(pos[0], pos[1]), end='\t')
            
    Z = dog.sense_position()
    zs.append(Z)
    vs.append(pos[1])
    
    pos = update(pos[0], pos[1], Z, sensor_variance)
    ps.append(pos[0])

    print('UPDATE: {: 10.4f} {: 10.4f}' .format(pos[0], pos[1]))

plt.plot(ps, label='filter')
plt.plot(zs, label='measurement')
plt.legend(loc='best')
plt.show()

plt.plot(vs)
plt.show()
