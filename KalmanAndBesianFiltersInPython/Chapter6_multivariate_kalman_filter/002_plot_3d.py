import utils.mkf_internal as mkf
import numpy as np
import matplotlib.pyplot as plt

img = mkf.plot_3d_covariance((2,17), np.array([[10, 0], [0, 4]]))

plt.show()
