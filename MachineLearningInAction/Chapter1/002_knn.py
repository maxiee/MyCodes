__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-

from numpy import *
import operator
import matplotlib.pyplot as plt

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

def file2matrix(filename):
    fr = open(filename)
    arrayOlines=fr.readlines()
    numberOfLines = len(arrayOlines)
    returnMat = zeros((numberOfLines,3))    # 限定矩阵仅有3列
    classLabelVector = []   #
    index = 0
    for line in arrayOlines:
        line = line.strip()     # 去掉回车符
        listFromLine = line.split('\t') # 将一整行数据打散为List
        returnMat[index,:]=listFromLine[0:3]    # 前三个表示特征的
        classLabelVector.append(int(listFromLine[-1]))  # 最后一个表示目标变量
        index += 1
    return returnMat, classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],\
                                     datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d"\
                % (classifierResult, datingLabels[i])
        if(classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))

if __name__ == "__main__":
    # TODO BUG 这里的数据集给错了，应该给测试数据集
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(normMat[:,1], normMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
    plt.show()
    datingClassTest()
