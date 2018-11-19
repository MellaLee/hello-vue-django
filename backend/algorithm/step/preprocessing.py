#暂时无需对数据进行预处理，此文件不需要运行
import pandas as pd
import os

date = '2018.06.04'
csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\backend/algorithm/download/originData/' + date  

def startRun():
    os.chdir(csv_file_path)
    files = os.listdir(csv_file_path)
    for filename in files:
        print (filename)
        df = pd.read_csv(filename, header=None, encoding='gbk')
        print (df.head())
        return

if __name__ == '__preprocessing':
    startRun()