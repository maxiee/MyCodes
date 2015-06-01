import matplotlib.pyplot as plt
import tushare.stock.trading as td

sz = td.get_hist_data(code='sh', start='2015-04-01', end='2015-05-22')
sz = sz[['close']]
close.plot()
plt.show()
