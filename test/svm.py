# 导入可进行矩阵计算的科学运算包
# import numpy as np
# import pylab as pl
# from sklearn import svm
# 打印进展信息
from time import time
import logging
import matplotlib.pyplot as plot

from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA

def basicExample():
	X = [[2, 0], [1, 1], [2, 3]]
	y = [0, 0, 1]

	# clf is short for classifier
	# SVC = supprt vector machine
	clf = svm.SVC(kernel='linear')
	clf.fit(X, y)

	print (clf) 
	# 输出支持向量
	print (clf.support_vectors_) 
	# supprt vector 在X中的索引
	print (clf.support_)
	# 每一类的支持向量的个数 
	print (clf.n_support_)
	# 预测新点
	print (clf.predict([2, 0]))

def linearableExample():
	# 随机生成40个样本点,包括线性可分的数据集与结果簇
	np.random.seed(0)
	X = np.r_[np.random.randn(20, 2) - [2, 2], np.random.randn(20, 2) + [2, 2]]
	Y = [0] * 20 + [1] * 20

	# 建立模型
	clf = svm.SVC(kernel='linear')
	clf.fit(X, Y)

	# 可视化分类的超平面
	# 该超平面原型为wx + b = 0，在此二维空间的例子中可写成w0x + w1y + b = 0,即 y = - w0x/w1 - b/w1
	# 获取向量W，二维
	w = clf.coef_[0]
	# 计算斜率
	a = -w[0] / w[1]
	# 随机选取部分点来进行可视化
	xx = np.linspace(-5, 5)
	yy = a * xx - (clf.intercept_[0]) / w[1]

	# 画出超平面外距离为1的两个平面
	b = clf.support_vectors_[0]
	yy_down = a * xx + (b[1] - a * b[0])
	b = clf.support_vectors_[-1]
	yy_up = a * xx + (b[1] - a * b[0])

	# plot 画图
	pl.plot(xx, yy, 'k-')
	pl.plot(xx, yy_down, 'k--')
	pl.plot(xx, yy_up, 'k--')

	pl.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80, facecolors='none')
	pl.scatter(X[:, 0], X[:, 1], c=Y, cmap=pl.cm.Paired)

	pl.axis('tight')
	pl.show()

def plot_gallery(images, titles, h, w, n_row=3, n_col=4):
    """Helper function to plot a gallery of portraits"""
    plot.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plot.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
    for i in range(n_row * n_col):
        plot.subplot(n_row, n_col, i + 1)
        plot.imshow(images[i].reshape((h, w)), cmap=plot.cm.gray)
        plot.title(titles[i], size=12)
        plot.xticks(())
        plot.yticks(())

def title(y_pred, y_test, target_names, i):
    pred_name = target_names[y_pred[i]].rsplit(' ', 1)[-1]
    true_name = target_names[y_test[i]].rsplit(' ', 1)[-1]
    return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

# 人脸识别
def linearlyInseparableExample():
	# 打印进展信息
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

	# 打印需要的数据集: 字典类型的对象
	lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)

	# -----------数据预处理-----------
	# n_samples实例个数 
	n_samples, h, w = lfw_people.images.shape
	X = lfw_people.data
	# 利用shape取得矩阵的列数，了解特征的维度
	n_features = X.shape[1]
	y = lfw_people.target
	target_names = lfw_people.target_names
	n_classes = target_names.shape[0]
	print("===== 数据集中信息 =====")
	print("数据个数(n_samples):", n_samples)
	print("特征个数，维度(n_features):", n_features)
	print("结果集类别个数(n_classes):", n_classes)

	# 将数据集分成训练集和测试集
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

	# PCA降维，减少特征值
	n_components = 150
	t0 = time()
	# n_components为要保留下来的特征数目
	pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
	print("pca done %0.3fs" % (time() - t0))

	# 转换成降维矩阵
	t0 = time()
	X_train_pca = pca.transform(X_train)
	X_test_pca  = pca.transform(X_test)
	print("data set to pca done %0.3fs" % (time() - t0))

	# 提取特征点
	eigenface = pca.components_.reshape((n_components, h, w))

	# 构造分类器
	t0 = time()
	param_grid = {
		"C": [1e3, 5e3, 1e4, 1e5],
		"gamma": [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]
	}

	clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid=param_grid)
	clf.fit(X_train_pca, y_train)
	print("fit done %0.3fs" % (time() - t0))
	print("best estimator found by grid search:")
	print(clf.best_estimator_)

	# 测试集上的准确率及可视化结果
	t0 = time()
	y_pred = clf.predict(X_test_pca)

	print(classification_report(y_test, y_pred, target_names=target_names))
	# 输出每一组测试集的真实标记和预测标记的对比
	print(confusion_matrix(y_test, y_pred, labels=range(n_classes)))

	# 可视化
	prediction_titles = [title(y_pred, y_test, target_names, i)
						for i in range(y_pred.shape[0])]
	plot_gallery(X_test, prediction_titles, h, w)
	# plot the gallery of the most significative eigenfaces
	eigenface_titles = ["eigenface %d" % i for i in range(eigenface.shape[0])]
	plot_gallery(eigenface, eigenface_titles, h, w)

	plot.show()

linearlyInseparableExample()