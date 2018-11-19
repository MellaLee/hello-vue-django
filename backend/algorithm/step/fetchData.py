#1. 爬虫得到数据
#使用了groupby+limit的方法，因为scroll不起作用
#可以考虑拿到所有文件，然后分成chunk人工groupBy
#出于小论文考虑，暂取了10000条数据
from urllib.request import urlopen
import json
import csv
import re 

date = '2018.06.04'
url = 'http://10.3.8.23/ext-api/v1/query?'
colNames = ['userNo', 'ip', 'domain', 'dstIp', 'args', 'time', 'classify']

def loadData(download=True):
    # fetch log from wrd-log-10.3.8.23
    if download:
        request = url + 'sql=SELECT * FROM urlevent-' + date + ' group by AUTH_ACCOUNT.keyword limit 10000'
        response = json.loads(urlopen(request).read().decode('utf-8'))
        if (response['status_code'] == 200):
            buckets = response['data']['buckets']
            userTotal = len(buckets)
            userDownload = 0
            for userBucket in buckets:
                userDownload = userDownload + 1
                if (userDownload <= 8480): continue
                if (userBucket['key'].isnumeric() is False): continue
                else:
                    downloadUserData(userBucket)
                    print (userDownload / userTotal)

def downloadUserData(userBucket):
    fileName = 'urllog-' + userBucket['key'] + '.csv'
    total = userBucket['doc_count'] 
    downloadSuccess = 0 
    scroll_id = 0
    with open('download/originData/' + date + '/' + fileName, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=colNames)
        while (downloadSuccess < total):
            if (scroll_id != 0):
                request = url + 'scroll_id=' + scroll_id
            else:
                request = url + 'sql=SELECT /*! USE_SCROLL(4000,60000) */ * FROM urlevent-' + date + ' where AUTH_ACCOUNT.keyword = ' + userBucket['key'] 
                response = json.loads(urlopen(request).read().decode('utf-8'))
            if (response['status_code'] == 200):
                content = response['data']
                hits = content['hits']
                scroll_id = content['scroll_id']
                downloadSuccess += len(hits)
                storeIntoCSV(hits, writer)

def storeIntoCSV(hits, writer):
    for hit in hits:
        source = hit['_source']
        try: 
            writer.writerow({
                'userNo': source['AUTH_ACCOUNT'],
                'ip': source['IP'],
                'domain': source['HOST'],
                'dstIp': source['DSTIP'],
                'args': source['URL'],
                'time': re.search(r"(\d{4}-\d{1,2}-\d{1,2}T\d{1,2}:\d{1,2})", source['@timestamp']).group(0).replace('T', ' '),
                'classify': source['APPID']
            })
        except Exception as e:
            print ('Error:', e, source)

def startRun():
    loadData(download=True)