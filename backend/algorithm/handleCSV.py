import os
import json
import pandas as pd
import numpy as np
from scipy.spatial import distance

import testStationarity as draw
# just for importing models of django
import sys
import django
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog 

csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\static/upload/' 
# TODO: choose a right var interval
# interval = '25T' 
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
                quantitativeLogList.append(QuantitativeLog(
                    url=domain,
                    urlSimilarOriginSeries=json.dumps((groupDf.values).tolist()),
                    timeSeries=json.dumps((date_only_array).tolist()),
                    user_id = userId,
                    similarEuc=eucDistance,
                    similarStd=np.std(groupDf.values)/np.mean(groupDf.values)
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
        print (i)
        notStat, totalSize = startQuantitative(i, dateMin, dateMax, groups, userId)
        if (notStat / totalSize < oldRatio):
            oldRatio = notStat / totalSize
            interval = i 
        print("failed:", i, oldRatio)

def readCsv(filename):
    df = pd.read_csv(filename, header=None, encoding='gbk', index_col=7, low_memory=False)
    df.index = pd.to_datetime(df.index)
    userId = User.objects.get(userNo=df[0].iloc[0]).id
    ts = df[4]
    dateMin = ts.index.min()
    dateMax = ts.index.max()
    # group by domain name
    findBestInterval(dateMin, dateMax, ts.groupby(df[4]), userId)

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