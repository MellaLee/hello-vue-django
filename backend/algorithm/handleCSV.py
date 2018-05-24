import os
import pandas as pd
import numpy as np

import testStationarity as draw

csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\static/upload/' 
# TODO: choose a right var interval
# interval = '25T' 
safeCheckTimes = 4 

def startRun():
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

