import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.random.seed(9876789)

# 构造数据
# beta 就是要拟合的参数
nsample = 100
sig = 0.5
x = np.linspace(0, 20, nsample)
X = np.c_[x, np.sin(x), (x-5)**2, np.ones(nsample)] # 设计变量
beta = np.array([0.5, 0.5, -0.02, 5.])
y_true = np.dot(X, beta)

# 构造测量数据
y = y_true + sig * np.random.normal(size=nsample)

model = sm.OLS(y, X)
results = model.fit()
params = results.params
#print(results.summary())

# 分量1 
plt.plot(x, params[0]*x, '--', label='sub-func 1')
# 分量2
plt.plot(x, params[1]*np.sin(x), '--', label='sub-func 2') 
# 分量3
plt.plot(x, params[2]*(x-5)**2, '--', label='sub-func 3')
# 分量4
plt.plot(x, params[3]*np.ones(nsample), '--', label='sub-func 4')
plt.plot(x, 
        params[0]*x +
        params[1]*np.sin(x) +
        params[2]*(x-5)**2 +
        params[3]*np.ones(nsample),
        label='fit')
plt.legend(loc='best')
# 数据点
plt.scatter(x, y, alpha=0.5)
plt.show()
