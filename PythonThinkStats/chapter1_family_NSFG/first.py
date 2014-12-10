__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-


import survey
import math

table = survey.Pregnancies()
table.ReadRecords()
print 'Number of pregnancies',  len(table.records)

# 活婴数量
outcome_sum = 0
birthord1_sum = 0;
birthordo_sum = 0;
prelengthord1_sum = 0;
prelengthordo_sum = 0;

for rec in table.records:
    if rec.outcome == 1:
        outcome_sum += 1
        if rec.birthord == 1:
            birthord1_sum += 1
            prelengthord1_sum += rec.prglength
        else:
            birthordo_sum += 1
            prelengthordo_sum += rec.prglength
print "活婴数量：", outcome_sum
print "第一胎数量：", birthord1_sum
print "非第一胎其他情况数量：",birthordo_sum
print "第一胎婴儿平均怀孕周期：", 1.0*prelengthord1_sum/birthord1_sum
print "其他婴儿平均怀孕周期：",1.0*prelengthordo_sum/birthordo_sum
print "两者差异：", 1.0*prelengthord1_sum/birthord1_sum - 1.0*prelengthordo_sum/birthordo_sum

'''
    first_answer.py 答案给的Difference in days
'''
mean_ord1 = 1.0*prelengthord1_sum/birthord1_sum
mean_ordo = 1.0*prelengthordo_sum/birthordo_sum
var_ord1 = 0
var_ordo = 0

for rec in table.records:
    if rec.outcome == 1:
        if rec.birthord == 1:
            var_ord1 += (rec.prglength-mean_ord1)**2
        else:
            var_ordo += (rec.prglength-mean_ordo)**2
var_ord1 /= (birthord1_sum-1)
var_ordo /= (birthordo_sum-1)

print "第一胎婴儿标准差：", math.sqrt(var_ord1)
print "其他婴儿标准差：", math.sqrt(var_ordo)

print "第一胎婴儿均值：", mean_ord1
print "其他婴儿均值：",mean_ordo
