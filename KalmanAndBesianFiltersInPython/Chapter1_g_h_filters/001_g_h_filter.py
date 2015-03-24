__author__ = 'Maxiee'
import numpy as np
import matplotlib.pyplot as plt
import utils.book_plots as bp

def g_h_filter(data, x0, dx, g, h, dt=1., pred=None):
    x = x0
    results = []
    for z in data:
        # Prediction Step
        x_est = x + (dx*dt)
        dx = dx

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


weights = [158.0, 164.2, 160.3, 159.9, 162.1, 164.6, 169.6, 167.4, 166.4, 171.0, 171.2, 172.6]
plt.xlim([0,10])
bp.plot_track([0,11],[160,172],label='Actual weight')
data = g_h_filter(data=weights, x0=160, dx=1, g=6./10, h=2./3, dt=1.)
plot_g_h_results(weights, data)
print(len(weights))