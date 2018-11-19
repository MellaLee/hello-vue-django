# 拿到设备类型参数列表
import os
import re
import pandas as pd

def startRun():
    csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\static/testUriDeviceType/' 
    os.chdir(csv_file_path)
    files = os.listdir(csv_file_path)
    for filename in files:
        df = pd.read_csv(filename, header=None, encoding='gbk', index_col=6, engine='python')
        df.index = pd.to_datetime(df.index)
        ts = df[5]
        list = []
        for args in ts.values:
            attr = re.findall(r"&((?!&).[^&=]+?)=iphone", args, flags=re.IGNORECASE)
            if len(attr) > 0:
                list.extend(attr)
        print (len(set(list)))

if __name__ == '__main__':
    startRun()