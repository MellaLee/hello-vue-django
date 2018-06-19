from urllib.request import urlopen
import json
import csv
import re 

def loadData(download=True):
    # fetch log from wrd-log-10.3.8.23
    date = '2018.06.09'
    url = 'http://10.3.8.23/ext-api/v1/query?'
    total = 0
    downloadSuccess = 0 
    scroll_id = 0
#    CSV_MAX_ROW = 1000000
    if download:
        colNames = ['userNo', 'ip', 'domain', 'dstIp', 'args', 'time', 'classify']
        fileName = 'urllog-' + date + '.csv'
        with open ('download/originData/' + fileName, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=colNames)
            while ((downloadSuccess == 0) | (downloadSuccess < total)):
                if (scroll_id != 0):
                    request = url + 'scroll_id=' + scroll_id
                else:
                    request = url + 'sql=SELECT * FROM urlevent-' + date + ' group by AUTH_ACCOUNT limit 5'
                    #request = url + 'sql=SELECT /*! USE_SCROLL(4000,60000) */ * FROM urlevent-' + date + 'groupBy userNo'
                print (request)
                response = json.loads(urlopen(request).read().decode('utf-8'))
                print (response)
                return
    #            fileName = 'urllog-' + date + '-' + (downloadSuccess // CSV_MAX_ROW) + '.csv'
                if (response['status_code'] == 200):
                    content = response['data']
                    hits = content['hits']
                    total = content['total']
                    scroll_id = content['scroll_id']
                    downloadSuccess += len(hits)
                    print (downloadSuccess / total)
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

if __name__ == '__fetchData':
    startRun()