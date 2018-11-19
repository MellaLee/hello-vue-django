# 小论文中的最后一个图
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdate
import xlsxwriter

csv_file_path = r'D:\GraduationThesis\graduation-code\hello-vue-django\static/upload/' 

def startRun():
	os.chdir(csv_file_path)
	files = os.listdir(csv_file_path)
	for filename in files:
		df = pd.read_csv(filename, header=None, encoding='gbk', index_col=7, low_memory=False)
		df.index = pd.to_datetime(df.index)
		ts = df[4]
		dateMin = ts.index.min()
		dateMax = ts.index.max()
		groups = ts.groupby(df[4])

		dates = pd.date_range(dateMin, dateMax, freq='5T')
		newTs = pd.Series(0, index=dates)
		
		for domain, groupDf in groups:
			if (domain == 'stat.funshion.net'):
				groupDf = pd.concat([newTs, groupDf.apply(revalue)]).resample('5T').sum()
				workbook = xlsxwriter.Workbook("异常访问.xlsx")
				worksheet = workbook.add_worksheet()
				headings = ['访问时间', '访问次数']
				data = [
					groupDf.values.tolist()
				]
				worksheet.write_row('A1', headings)

				worksheet.write_column('A2', range(0, len(data[0])))
				worksheet.write_column('B2', data[0])

				workbook.close()
				return
				mpl.rcParams['font.sans-serif']=['SimSun'] #指定默认字体 SimHei为黑体
				mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
				plt.xticks(pd.date_range(groupDf.index[0],groupDf.index[-1], freq='2H'))
				plt.gca().xaxis.set_major_formatter(mdate.DateFormatter('%m-%d %H:%M'))
				plt.xlabel('访问时间', fontsize=12)
				plt.ylabel('访问次数', fontsize=12)
				plt.plot(groupDf.index, groupDf.values.tolist(), label="某用户访问URL-b")
				plt.legend(loc="upper right")
				plt.show()

def revalue(x):
	return 1

if __name__ == '__main__':
	startRun()
