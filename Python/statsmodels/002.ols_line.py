import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.random.seed(9876789)

# 构造数据
# beta 就是要拟合的参数
nsample = 100
x = np.linspace(0, 10, 100) # 设计变量
beta = np.array([1, 2])
e = np.random.normal(size=nsample)

X = sm.add_constant(x) #X左侧添加一列全1列
print(X)
# 构造测量数据
y = np.dot(X, beta) + e

# 拟合
model = sm.OLS(y, X)
results = model.fit()
# 拟合报告
print(results.summary())
# 拟合参数, list
# print(results.params)

# 绘制测量数据
plt.scatter(x, y, alpha=0.5)
# 绘制拟合直线
plt.plot(x, results.params[0] + results.params[1] * x, 'r')
plt.show()
