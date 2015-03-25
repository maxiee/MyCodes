__author__ = 'Maxiee'
import numpy.random as random
import matplotlib.pyplot as plt

def my_g_h_filter(data, x0, dx0, g, h, dt=1, pred=None):
    # data - 观测数据
    # x0 - 初始状态
    # dx0 - 初始变化率(速度)
    # g,h - 相关参数
    # pred - 是个List，用来存放预测值
    x = x0
    dx = dx0
    results = []

    for z in data:
        x_est = x + (dx*dt)

        if pred is not None:
            pred.append(x_est)

        residual = z - x_est
        dx = dx + h * residual / dt
        x = x_est + g * residual
        results.append(x)
    return results

# 考虑有一个小汽车，以10m/s匀速运动，从0位置处出发,仿真50s
t = [i for i in range(50)]
real = [i*10 for i in t]
# 测量误差为20m吧
measurements = [i + random.randn()*20 for i in real]
# 打印真实状态与测量
# plt.plot(t,real,t,measurements)
# plt.show()
# 下面我该用滤波了
pred = []
g_h_result = my_g_h_filter(measurements, 0, 20, 0.5, 0.2,1,pred)
plt.plot(t,real,t,measurements,t,g_h_result,t,pred)
plt.legend(['real','mea', 'filtering','pred'],loc=2)
plt.show()