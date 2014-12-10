__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

import thinkstats
import math

pumpkin_weight = [1, 1, 1, 3, 3, 591]

print "均值：",thinkstats.Mean(pumpkin_weight)
print "方差：",thinkstats.Var(pumpkin_weight)
print "标准差：",math.sqrt(thinkstats.Var(pumpkin_weight))