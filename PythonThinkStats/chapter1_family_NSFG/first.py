__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-


import survey

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
    first_answer.py 答案给的Difference in days结果不对啊= =
'''