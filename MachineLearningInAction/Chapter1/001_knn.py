__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX,dataSet, labels, k):
    '''

    :param inX: 新的未知数据
    :param dataSet: 已知数据集
    :param labels:  已知目标变量
    :param k:
    :return:
    '''
    dataSetSize = dataSet.shape[0]
    # 计算距离
    # tile 重复矩阵 inX 来构建新矩阵
    diffMat = tile(inX, (dataSetSize,1)) - dataSet # 算出各特征之差
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis = 1)
    distances = sqDistances ** 0.5 # 算出未知数据到各已知数据的距离值
    sortedDistIndicies = distances.argsort() # 排序
    classCount = {}
    # 选择距离最近的K个点
    for i in range(k):
        # 这里是一个频率统计
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key = operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

if __name__ == "__main__":
    group,labels = createDataSet()
    print classify0([0,0], group, labels, 3)
