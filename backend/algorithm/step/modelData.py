# numpy支持大量的维度数组与矩阵运算
import numpy as np
from sklearn.mixture import GaussianMixture as GMM 
from sklearn.cluster import KMeans
from sklearn import preprocessing
from scipy import linalg
import itertools
# import calDB
from sklearn.model_selection import StratifiedKFold
import matplotlib.pyplot as plt
import matplotlib as mpl
# from sklearn.cluster import KMeans
# just for importing models of django
import os
import sys
import django
import random
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog
from backend.algorithm.visualize import pltCharacter

colors = ['navy', 'darkorange']
labels = ['善意访问', '恶意访问']
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
def make_ellipses(gmm, ax):
	for n, color in enumerate(colors):
		if gmm.covariance_type == 'full':
			covariances = gmm.covariances_[n][:2, :2]
		elif gmm.covariance_type == 'tied':
			covariances = gmm.covariances_[:2, :2]
		elif gmm.covariance_type == 'diag':
			covariances = np.diag(gmm.covariances_[n][:2])
		elif gmm.covariance_type == 'spherical':
			covariances = np.eye(gmm.means_.shape[1]) * gmm.covariances_[n]
		v, w = np.linalg.eigh(covariances)
		u = w[0] / np.linalg.norm(w[0])
		angle = np.arctan2(u[1], u[0])
		angle = 180 * angle / np.pi  # convert to degrees
		v = 2. * np.sqrt(2.) * np.sqrt(v)
		ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
								  180 + angle, color=color)
		ell.set_clip_box(ax.bbox)
		ell.set_alpha(0.5)
		ax.add_artist(ell)
		ax.set_aspect('equal', 'datalim')

def fetchClusterData():
	goodlog = QuantitativeLog.objects.filter(label=0)
	badlog = QuantitativeLog.objects.filter(label=1)
	logTotal = len(goodlog) + len(badlog)

	X_goodlog = [list(x) for x in goodlog.values_list('similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability', 'sameArgsDiversity', 'webClassify')]
	Y_goodlog =[x[0] for x in goodlog.values_list('label')]
	id_goodlog = [x[0] for x in goodlog.values_list('id')] 

	X_badlog = [list(x) for x in badlog.values_list('similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability', 'sameArgsDiversity', 'webClassify')]
	Y_badlog = [x[0] for x in badlog.values_list('label')]
	id_badlog = [x[0] for x in badlog.values_list('id')] 

	each_type_num = int(logTotal * 0.6 * 0.8 / 2)
	X_cluster = X_goodlog[:each_type_num] + X_badlog[:each_type_num]
	Y_cluster = Y_goodlog[:each_type_num] + Y_badlog[:each_type_num]
	id_log = id_goodlog[:each_type_num] + id_badlog[:each_type_num]
	return X_cluster, Y_cluster, id_log

def storeIntoSql(id, cluster_label):
	allModel = QuantitativeLog.objects.filter(pk__in=id)
	i = 0
	for index, model in enumerate(allModel):
		i += 1
		if (i % 10000 == 0):
			print (i)
		model.cluster_label = cluster_label[index]
		model.save()
		
# 数据拆分比例说明
# 训练：验证：测试 = 6：2：2
# 如果数据量为a
# 则聚类可用数据为0.6a,拆分比为0.36a:0.12a:0.12a
# svm数据比为0.6a:0.2a:0.2a
def startRun():
	# 获取数据
	X_cluster, Y_cluster, id_log = fetchClusterData()

	# 标准化数据 
	X_cluster = np.array(X_cluster, dtype=np.float64)
	Y_cluster = np.array(Y_cluster, dtype=np.float64)
	for index, x in enumerate(X_cluster):
		X_cluster[index] = preprocessing.scale(x)

	# 拆分数据
	skf = StratifiedKFold(n_splits=4)
	train_index, test_index = next(iter(skf.split(X_cluster, Y_cluster)))
	x_train = X_cluster[train_index]
	y_train = Y_cluster[train_index]
	x_test = X_cluster[test_index]
	y_test = Y_cluster[test_index]

	# Gmm model
	cv_types = ['spherical', 'tied', 'diag', 'full']
	cv_types_name = {'spherical':'球面协方差矩阵', 'tied': '相同的完全协方差矩阵', 'diag': '对角协方差矩阵', 'full':'完全协方差矩阵'}
	n_classes = 2
	estimators = dict((cov_type, GMM(n_components=n_classes, 
		covariance_type=cov_type, max_iter=20, random_state=0))
		for cov_type in cv_types)

	n_estimators = len(estimators)
	# figsize（宽，高）
	# plt.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
	#				left=.01, right=.99)

	# 遍历索引序列
	for index, (name, estimator) in enumerate(estimators.items()):
		estimator.means_init = np.array([x_train[y_train == i].mean(axis=0)
										for i in range(n_classes)])
		estimator.fit(x_train)
		#subplot(行数， 列数， 每行的第几个图像)
		plt.figure(index + 1, figsize=(3, 3))
		h = plt.subplot(1, 1, 1)
		make_ellipses(estimator, h)

		for n, color in enumerate(colors):
			data = X_cluster[Y_cluster == n]
			plt.scatter(data[:, 0], data[:, 1], s=0.8, color=color, label=labels[n])

		# Plot the test data with crosses
		for n, color in enumerate(colors):
			data = x_test[y_test == n]
			plt.scatter(data[:, 0], data[:, 1], marker='x', color=color)

		y_train_pred = estimator.predict(x_train)
		train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
		plt.text(0.05, 0.9, '训练集准确率: %.1f' % train_accuracy, transform=h.transAxes)

		y_test_pred = estimator.predict(x_test)
		test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
		plt.text(0.05, 0.8, '测试集准确率: %.1f' % test_accuracy, transform=h.transAxes)
		plt.xticks(())
		plt.yticks(())
		plt.title(cv_types_name[name])
		plt.legend(scatterpoints=1, loc='lower right', prop=dict(size=12))
		#if (name == 'diag'):
		#	storeIntoSql(id_log, np.append(y_train_pred, y_test_pred))
		print (name + ' done')

	plt.show()