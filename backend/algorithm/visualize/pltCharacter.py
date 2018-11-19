import matplotlib.pyplot as plt
import matplotlib as mpl
# 生成'聚类标记'页面的python图表，可用作页面展示
def plot(cluster1, cluster2, chartName):
	mpl.rcParams['font.sans-serif']=['SimSun'] #指定默认字体 SimHei为黑体
	mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
	x = range(1, 1000)
	plt.xlabel('用户访问编号', fontsize=12)
	plt.ylabel(chartName, fontsize=12)
	plt.plot(x, cluster1[500:1499], label="恶意访问")
	plt.plot(x, cluster2[500:1499], label="善意访问")
	# plt.ylim(ymin=-500, ymax=3000)
	plt.legend(loc="upper right")
	plt.show()