import os
import json
import pandas as pd
import numpy as np
import Levenshtein
import scipy
import matplotlib.pyplot as plt
from scipy.spatial import distance
import scipy.cluster.hierarchy as sch
import scipy.stats as ss

import testStationarity as draw
# just for importing models of django
import sys
import django
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog, UrlArgsTestMethod 

csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\static/upload/' 
# TODO: choose a right var interval
# interval = '10T' 
safeCheckTimes = 4 

def startQuantitative(i, dateMin, dateMax, groups, userId):
    dates = pd.date_range(dateMin, dateMax, freq=str(i) + 'T')
    newTs = pd.Series(0, index=dates)
    notStat = 0
    totalSize = 0 
    quantitativeLogList = []
    for domain, groupDf in groups:
        # get a timeSeries every $interval following the [min, max]
        groupDf = pd.concat([newTs, groupDf.apply(revalue)]).resample(str(i) + 'T').sum()
        if (groupDf.size > safeCheckTimes):
            totalSize += 1 
            ifStat = draw.testStationarity(groupDf)
            if (ifStat is False):
                notStat += 1
            else:
                oldValue = -1
                eucDistance = 0
                for value in groupDf:
                    if (oldValue >= 0):
                        eucDistance += distance.euclidean(oldValue, value)
                    oldValue = value
                        
                pydate_array = groupDf.index.to_pydatetime()
                date_only_array = np.vectorize(lambda s: s.strftime('%m-%d %H:%M'))(pydate_array )
                #cal urlargsEntropy

                quantitativeLogList.append(QuantitativeLog(
                    url=domain,
                    urlSimilarOriginSeries=json.dumps((groupDf.values).tolist()),
                    timeSeries=json.dumps((date_only_array).tolist()),
                    user_id = userId,
                    similarEuc=eucDistance,
                ))
                #valuesT = values.reshape(-1, 1)
                #eucDistance = calEuclidean(values, valuesT)
    QuantitativeLog.objects.all().delete()
    for i in range(0, len(quantitativeLogList), 200):
        QuantitativeLog.objects.bulk_create(quantitativeLogList[i:i + 200])
    return notStat, totalSize

def findBestInterval(dateMin, dateMax, groups, userId):
    oldRatio = 1 
    interval = 0
    for i in range(10, 20, 10):
        notStat, totalSize = startQuantitative(
            i, dateMin, dateMax, groups, userId)
        if (notStat / totalSize < oldRatio):
            oldRatio = notStat / totalSize
            interval = i
        print("failed:", i, oldRatio)

def startCalUrlArgsEntropy(urlArgs, userId):
    urlArgsList = []
    for domain, args in urlArgs:
        argsValues = args.values
        lastArgs = 0
        total = 0
        for args in argsValues:
            if (lastArgs != 0):
                total += similarUrlAgrs(lastArgs, args[0])
            else:
                lastArgs = args[0]
        # calculate entropy
        hierarchyDisMat = sch.distance.pdist(argsValues, lambda str1, str2:  1 - similarUrlAgrs(str1[0], str2[0]))
        if (len(hierarchyDisMat) == 0):
            method2 = 0
        else:
            Z = sch.linkage(hierarchyDisMat, method='average')
            hierarchyRes = sch.fcluster(Z, 0.1) 
            unique, counts = np.unique(hierarchyRes, return_counts=True)
            method2=ss.entropy(counts)

        QuantitativeLog.objects.filter(user_id=userId, url=domain).update(urlArgsEntropy=method2)

#        urlArgsList.append(UrlArgsTestMethod(
#            url=domain,
#            args=argsValues,
#            method1=total / len(argsValues),
#            method2=method2
#        ))
#    UrlArgsTestMethod.objects.all().delete()
#    for i in range(0, len(urlArgsList), 200):
#        UrlArgsTestMethod.objects.bulk_create(urlArgsList[i:i + 200])

def find_lcsubstr(s1, s2):   
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]  #生成0矩阵，为方便后续计算，比字符串长度多了一列  
    mmax=0   #最长匹配的长度  
    p=0  #最长匹配对应在s1中的最后一位  
    for i in range(len(s1)):  
        for j in range(len(s2)):  
            if s1[i]==s2[j]:  
                m[i+1][j+1]=m[i][j]+1  
                if m[i+1][j+1]>mmax:  
                    mmax=m[i+1][j+1]  
                    p=i+1  
    #return s1[p-mmax:p],mmax   #返回最长子串及其长度  
    return mmax   #返回最长子串及其长度  

def similarUrlAgrs(str1, str2):
    lcs=find_lcsubstr(str1, str2)  
    ld=Levenshtein.distance(str1, str2)
    return (lcs / (ld + lcs))

def readCsv(filename):
    df = pd.read_csv(filename, header=None, encoding='gbk', index_col=7, low_memory=False)
    df.index = pd.to_datetime(df.index)
    userId = User.objects.get(userNo=filename.split('.')[0].split('-')[1]).id
    args = sys.argv
    if (args[1] == 'first'):
        ts = df[4]
        dateMin = ts.index.min()
        dateMax = ts.index.max()
        # group by domain name
        findBestInterval(dateMin, dateMax, ts.groupby(df[4]), userId)
    elif (args[1] == 'second'):
        urlArgs = df.loc[:, [6]].groupby(df[4])
        startCalUrlArgsEntropy(urlArgs, userId)
    elif (args[1] == 'psd'):
        ts = df[4]
        dateMin = ts.index.min()
        dateMax = ts.index.max()
        dates = pd.date_range(dateMin, dateMax, freq='10T')
        newTs = pd.Series(0, index=dates)

        for domain, groupDf in ts.groupby(df[4]):
            groupDf = pd.concat([newTs, groupDf.apply(revalue)]).resample('10T').sum()
            hour = groupDf.index.hour
            groupDf = groupDf[(1 <= hour) & (hour <= 5)]
            sampRat = len(groupDf) 
            T = 1 
            f = np.linspace(0, sampRat, T*sampRat, endpoint=False)  
            ff = np.fft.fft(groupDf)  
            ff = np.abs(ff)  
            ff = ff*2/sampRat/T 
            QuantitativeLog.objects.filter(user_id=userId, url=domain).update(abnormalTimeProbability=np.std(ff))

def startRun():
    os.chdir(csv_file_path)
    files = os.listdir(csv_file_path)
    for filename in files:
        readCsv(filename)

def calEuclidean(A, B):
    A.shape = (A.shape[0], 1)
    BT = B.transpose()
    # vecProd = A * BT
    vecProd = np.dot(A,BT)
    SqA =  A**2
    sumSqA = np.matrix(np.sum(SqA, axis=1))
    sumSqAEx = np.tile(sumSqA.transpose(), (1, vecProd.shape[1]))

    SqB = B**2
    sumSqB = np.sum(SqB, axis=1)
    sumSqBEx = np.tile(sumSqB, (vecProd.shape[0], 1))    
    SqED = sumSqBEx + sumSqAEx - 2*vecProd
    SqED[SqED<0]=0   
    ED = np.sqrt(SqED)
    return ED

def startRunOld():
    os.chdir(csv_file_path)
    files = os.listdir(csv_file_path)
    for filename in files:
        df = pd.read_csv(filename, header=None, encoding='gbk', index_col=7)
        df.index = pd.to_datetime(df.index)
        ts = df[4]
        # group by domain name
        groups = ts.groupby(df[4])
        oldRatio = 1 
        interval = 0
        for i in range(10, 30): 
            notStat = 0
            totalSize = 0 
            for domain, groupDf in groups:
                # get a timeSeries every $interval
                groupDf = groupDf.apply(revalue).resample(str(i) + 'T').sum()
                if (groupDf.size > safeCheckTimes):
                    totalSize += 1 
                    ifStat = draw.testStationarity(groupDf)
                    if (ifStat is False):
                        notStat += 1
            if (notStat / totalSize < oldRatio):
                oldRatio = notStat / totalSize
                interval = i 
        print("failed:", i, oldRatio)

def revalue(x):
    return 1

if __name__ == '__handleCSV':
    startRun()