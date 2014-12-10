__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

'''
    程序功能：绘制第一胎与非第一胎频数直方图
'''
import survey
import matplotlib.pyplot as pyplot

table = survey.Pregnancies()
table.ReadRecords()
count = len(table.records)

freq1rd = {}
freqord = {}

for rec in table.records:
    if rec.outcome == 1:
        if rec.birthord == 1:  # 统计第一胎频数
            freq1rd[rec.prglength] = freq1rd.get(rec.prglength,0)+1
        else:  # 统计其他频数
            freqord[rec.prglength] = freqord.get(rec.prglength,0)+1

width = 0.35
pyplot.bar(freq1rd.keys(),freq1rd.values(),width,color='r')
pyplot.bar([i+width for i in freqord.keys()],freqord.values(),width)
pyplot.show()