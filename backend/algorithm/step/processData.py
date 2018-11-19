#2. 处理数据, 量化特征
import re
import json
import Levenshtein
import numpy as np
import pandas as pd
import scipy.stats as ss
from step import testStationarity as draw
from scipy.spatial import distance
import scipy.cluster.hierarchy as sch
# just for importing models of django
import os
import sys
import django
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog

date = '2018.06.04'
safeCheckTimes = 4 
csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\backend/algorithm/download/originData/' + date  

def readCsv(fileName, userId):
    df = pd.read_csv(fileName, header=None, encoding='gbk', index_col=5, low_memory=False)
    df.index = pd.to_datetime(df.index)
    result = {}
    #1. cal '时间窗口内域名访问相似度' 
    result = calSimilarEuc(df, userId)
    #2. cal 'URL参数信息熵'
    result = calUrlArgsEntropy(df.loc[:, [6]].groupby(df[2]), userId, result)
    #3. cal '异常时间频发度' 
    result = calAbnormalTimeFrequ(df[2], df, result)
    #4. cal 'uri同一参数一致性'
    result = calSameArgsDiversity(fileName, result)
    #5. cal '网页分类'
    result = calWebClassify(df[6], result, df)
    quantitativeLogList = []
    for res in result:
        log = result[res]
        quantitativeLogList.append(QuantitativeLog(
            url=log['url'],
            user_id = userId,
            similarEuc=log['similarEuc'],
            urlArgsEntropy=log['urlArgsEntropy'],
            abnormalTimeProbability=log['abnormalTimeProbability'],
            sameArgsDiversity=log['sameArgsDiversity'],
            webClassify=log['webClassify']
        ))
    for i in range(0, len(quantitativeLogList), 200):
        QuantitativeLog.objects.bulk_create(quantitativeLogList[i:i + 200])

def calWebClassify(ts, result, df):
    for domain, groupDf in ts.groupby(df[2]):
        if domain in result:
            classifies = groupDf.values.tolist()
            dict = {x: classifies.count(x) for x in classifies}
            total = 0
            wwwCount = 0
            for classify, val in dict.items():
                if (classify == 'WWW'):
                    wwwCount += val
                total += val
                result[domain]['webClassify'] = round(val / total, 4)
    return result

def calSameArgsDiversity(fileName, resultDict):
    df = pd.read_csv(fileName, header=None, encoding='gbk', index_col=5, low_memory=False)
    DEVICE_LIST = ['clientType', 'sOsType', 'sver', 'mo', 'ta_tn', 'platform_name', 'brand', 'client', 'ctype', 'deviceName', 
    'fr', 'sysname', 'ua_model', 'plf', 'atsp', 'mt', 'dt', 'phoneModel', 'hw', 'secure_p', 'cpu', 'machine', 'user_client', 
    'ver', 'deviceType', 'dname', '_device', '__os__', 'sv', 'phone_model', 'pf_ex', 'bdsv', 'client_type', 'wm_ctype', 
    'share_medium', 'devicetype', 'ch', '_dev', 'msg', 'systemName', 'dm', 'result8', 'tn', 'channel', 'brand_type', 
    'sys_ver_type', 'device_type', '_appid', 'device', 'word', 'dsp', 'mn', 'cad[device_model]', 'snapid', 'device_platform', 
    'clientOs', 'hwtype', 'deviceModel', 'dev', 'mod', 'pn', 'Os', 'dspName', 'phoneos', 'pid', 'result', 'devtype', 'ism', 
    'term', 'category', 'dev_ua', 'PHONEMODEL', 'device_name', 'md', 'modelName', '_platform', 'result9', 'dev_model', 
    'userDeviceModel', 'hm', 'plat', 'os', 'wm_dtype', 'devicename', 'manufacturer', 'mfov', 'pv', 'os_name', 'name', 'ua', 
    'ex3', 'phonebrand', 'facturer', 'iphonetype', 'version', 'submodel', 'mb', 'firstChannel', 'mobi_app', 'platform', 
    'result7', 'device_model', 'hv', 'iosModel', 'model', 'pm', 'up', 'pf', 'utm_medium', 'mxh', 'location', 'c_device', 
    'cl', 'DeviceModel', 'deviceinfo', 'device_version', 'mi', 'os_info', 'result5', 'useragent']

    result = {}
    for domain, dataframe in df.groupby(df[2]):
        if domain in resultDict:
            domainRes = []
            for deviceAttr in DEVICE_LIST:
                reg = r"&" + deviceAttr + "=(.+?)&"
                for args in dataframe[4].values:
                    matchRes = re.findall(reg, args)
                    if (len(matchRes) > 0):
                        domainRes.extend(matchRes) 
            if (len(set(domainRes)) > 1):
                result[domain] = len(set(domainRes)) / len(domainRes)
            else:
                result[domain] = 0 
            resultDict[domain]['sameArgsDiversity'] = round(result[domain], 4)
    return resultDict

def calAbnormalTimeFrequ(ts, df, result):
    dateMin = ts.index.min()
    dateMax = ts.index.max()
    dates = pd.date_range(dateMin, dateMax, freq='10T')
    newTs = pd.Series(0, index=dates)

    for domain, groupDf in ts.groupby(df[2]):
        if domain in result:
            groupDf = pd.concat([newTs, groupDf.apply(revalue)]).resample('10T').sum()
            hour = groupDf.index.hour
            groupDf = groupDf[(1 <= hour) & (hour <= 5)]
            sampRat = len(groupDf) 
            if (sampRat == 0):
                result[domain]['abnormalTimeProbability']=0
            else:
                T = 1 
                f = np.linspace(0, sampRat, T*sampRat, endpoint=False)  
                ff = np.fft.fft(groupDf)  
                ff = np.abs(ff)  
                ff = ff*2/sampRat/T 
            #QuantitativeLog.objects.filter(user_id=userId, url=domain).update()
                result[domain]['abnormalTimeProbability']=np.std(ff)
    return result

def calUrlArgsEntropy(urlArgs, userId, result):
    for domain, args in urlArgs:
        if domain in result:
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

            result[domain]['urlArgsEntropy'] = method2
    return result

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

def calSimilarEuc(df, userId):
    ts = df[2]
    dateMin = ts.index.min()
    dateMax = ts.index.max()
    # group by domain name
    similarEuc = findBestInterval(dateMin, dateMax, ts.groupby(df[2]), userId)
    return similarEuc

def findBestInterval(dateMin, dateMax, groups, userId):
    oldRatio = 1 
    interval = 0
    result = {} 
    for i in range(10, 20, 10):
        notStat, totalSize, similarEuc = startQuantitative(
            i, dateMin, dateMax, groups, userId)
        if (notStat / totalSize < oldRatio):
            oldRatio = notStat / totalSize
            interval = i
            result = similarEuc
        print("failed:", i, oldRatio)
    return result

def startQuantitative(i, dateMin, dateMax, groups, userId):
    dates = pd.date_range(dateMin, dateMax, freq=str(i) + 'T')
    newTs = pd.Series(0, index=dates)
    notStat = 0
    totalSize = 0 
    quantitativeLogDict = {} 
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
                        
                #cal urlargsEntropy
                quantitativeLogDict[domain] = {
                    'url': domain,
                    'user_id': userId,
                    'similarEuc': eucDistance,
                }
    return notStat, totalSize, quantitativeLogDict

def revalue(x):
    return 1

def startRun():
    os.chdir(csv_file_path)
    files = os.listdir(csv_file_path)
    for fileName in files:
        user, created = User.objects.get_or_create(
            userNo=fileName.split('.')[0].split('-')[1])
        if (created):
            user.save()
        readCsv(fileName, user.id)