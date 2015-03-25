__author__ = 'Maxiee'
import utils.book_plots as bp
import numpy.random as random
import matplotlib.pyplot as plt
import numpy as np



def g_h_filter(data, x0, dx, g, h, dt=1., pred=None):
    x = x0
    results = []
    for z in data:
        print(dx)
        # Prediction Step
        x_est = x + (dx*dt)
        # 这句话什么意思？去掉也是一样，dx的值本来就是变化的
        # dx = dx

        if pred is not None:
            pred.append(x_est)

        # Update Step
        residual = z - x_est
        dx = dx    + h * (residual) / dt
        x  = x_est + g * residual

        results.append(x)

    return np.asarray(results)

def plot_g_h_results(measurements, filtered_data,
                     title="", z_label="Scale",):
    bp.plot_measurements(measurements, label=z_label)
    bp.plot_filter(filtered_data)
    plt.legend(loc=4)
    plt.title(title)
    plt.gca().set_xlim(left=0,right=len(measurements))
    plt.show()

def gen_data(x0, dx, count, noise_factor):
    return [x0 + dx*i + random.randn()*noise_factor for i in range(count)]

measurements = gen_data(0, 1, 30, 1)
data = g_h_filter(data=measurements, x0=0, dx=1, dt=1, g=0.2, h=0.02)
plot_g_h_results(measurements, data)