import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.random.seed(9876789)

# 构造数据
# beta 就是要拟合的参数
nsample = 100
x = np.linspace(0, 10, 100)
X = np.column_stack((x, x**2)) # 设计变量
beta = np.array([1, 0.1, 5])
e = np.random.normal(size=nsample)*50

X = sm.add_constant(X) #X左侧添加一列全1列
# 构造测量数据
y = np.dot(X, beta) + e

model = sm.OLS(y, X)
results = model.fit()
#print(results.summary())

# 一阶分量
plt.plot(x, results.params[1]*x, '--', label='1st order')
# 二阶分量
plt.plot(x, results.params[2]*x*x, '--', label='2nd order') 
# 拟合曲线
plt.plot(x, 
        results.params[0] + 
        results.params[1] * x + 
        results.params[2] * x * x, label='fit')
plt.legend(loc='best')
# 数据点
plt.scatter(x, y, alpha=0.5)
plt.show()
