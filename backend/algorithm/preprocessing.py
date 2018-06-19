import pandas as pd
import os

csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\backend/algorithm/download/originData' 

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