__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import thinkstats
import math
import Pmf
import matplotlib.pyplot as pyplot

pumpkin_weight = [1, 1, 1, 3, 3, 8]

print "均值：",thinkstats.Mean(pumpkin_weight)
print "方差：",thinkstats.Var(pumpkin_weight)
print "标准差：",math.sqrt(thinkstats.Var(pumpkin_weight))

hist = Pmf.MakeHistFromList(pumpkin_weight)

# 返回众数
mode = sorted(hist.Values())[0]
print "众数为：%d 频数为：%d" % (mode, hist.Freq(mode))

# 绘制直方图
vals, freqs = hist.Render()
rectangles = pyplot.bar(vals, freqs)
pyplot.show()