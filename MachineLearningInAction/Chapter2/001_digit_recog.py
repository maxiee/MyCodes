__author__ = 'Maxiee'
# -*- coding: UTF-8 -*-
from numpy import *
import operator
from os import listdir

def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i +j] = int(lineStr[j])
    return returnVect

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

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if(classifierResult != classNumStr):    errorCount += 1.0
    print"\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount / float(mTest))

if __name__ == "__main__":
    testVector = img2vector('testDigits/0_13.txt')
    print testVector[0, 0:31]
    handwritingClassTest()

