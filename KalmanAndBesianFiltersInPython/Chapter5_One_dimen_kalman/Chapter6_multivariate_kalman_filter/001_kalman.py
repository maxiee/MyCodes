# -*- coding: utf-8 -*-
import numpy as np
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

dog_filter = KalmanFilter(dim_x=2, dim_z=1)

dog_filter.x = np.array([0., 0.])
dog_filter.F = np.array([[1, 1], [0, 1]])
dog_filter.H = np.array([[1,0]])
dog_filter.R *= 500
dog_filter.Q = Q_discrete_white_noise(2, dt=0.1, var=0.1)
dog_filter.P *= 500
