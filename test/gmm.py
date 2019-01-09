import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

colors = ['navy', 'turquoise', 'darkorange']
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

def test2():
	from sklearn import datasets
	from sklearn.mixture import GaussianMixture as GMM
	from sklearn.model_selection import StratifiedKFold
	iris = datasets.load_iris()
	skf = StratifiedKFold(n_splits=4)
	train_index, test_index = next(iter(skf.split(iris.data, iris.target))) # iter获取迭代器，next通过迭代器获取下一条数据
	X_train = iris.data[train_index]
	y_train = iris.target[train_index]

	X_test = iris.data[test_index]
	y_test = iris.target[test_index]

	n_classes = len(np.unique(y_train))

	# start to train gmm
	estimators = dict((cov_type, GMM(n_components=n_classes, 
		covariance_type=cov_type, max_iter=20, random_state=0))
		for cov_type in ['spherical', 'diag', 'tied', 'full'])

	n_estimators = len(estimators)
	# figsize（宽，高）
	plt.figure(figsize=(3 * n_estimators // 2, 6))
	plt.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
					left=.01, right=.99)

	# 遍历索引序列
	for index, (name, estimator) in enumerate(estimators.items()):
		estimator.means_init = np.array([X_train[y_train == i].mean(axis=0)
										for i in range(n_classes)])
		estimator.fit(X_train)
		#subplot(行数， 列数， 每行的第几个图像)
		h = plt.subplot(2, n_estimators // 2, index + 1)
		make_ellipses(estimator, h)

		for n, color in enumerate(colors):
			data = iris.data[iris.target == n]
			plt.scatter(data[:, 0], data[:, 1], s=0.8, color=color,
						label=iris.target_names[n])
		# Plot the test data with crosses
		for n, color in enumerate(colors):
			data = X_test[y_test == n]
			plt.scatter(data[:, 0], data[:, 1], marker='x', color=color)

		y_train_pred = estimator.predict(X_train)
		train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
		plt.text(0.05, 0.9, 'Train accuracy: %.1f' % train_accuracy,
				transform=h.transAxes)

		y_test_pred = estimator.predict(X_test)
		test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
		plt.text(0.05, 0.8, 'Test accuracy: %.1f' % test_accuracy,
				transform=h.transAxes)
		plt.xticks(())
		plt.yticks(())
		plt.title(name)
	plt.legend(scatterpoints=1, loc='lower right', prop=dict(size=12))

	plt.show()

def test1():
	from mpl_toolkits.mplot3d import Axes3D

	result = {}
	# 构建示例数据集
	from sklearn.datasets.samples_generator import make_blobs
	X, y_true = make_blobs(n_samples=10000, centers=2, cluster_std=0.60, random_state=0, n_features=5)
	# n_samples为样本个数，center表示产生数据的中心点，cluster_std表示数据集的标准差，random_state随机产生的结果与其值有关

	# gmm
	from sklearn.mixture import GaussianMixture as GMM
	gmm = GMM(n_components=2, covariance_type='spherical').fit(X)
	# covariance_type即通过EM算法估算参数时使用的协方差类型，默认full
	result['gmm'] = gmm.predict(X)

	# kmeans
	from sklearn.cluster import KMeans
	from scipy.spatial.distance import cdist
	result['kmeans'] = KMeans(n_clusters=2).fit_predict(X)

	# 性能指标
	from sklearn import metrics

	def output(type, y_pred): 
		print (type)
		print("accuracy_score:", metrics.accuracy_score(y_true, y_pred))
		print("precision_score:", metrics.precision_score(y_true, y_pred))
		print("recall_score:", metrics.recall_score(y_true, y_pred))
		fpr, tpr, thresholds = roc_curve()

	for itemIndex in result:
		output(itemIndex, result[itemIndex])

	# fig = plt.figure()
	# ax = fig.add_subplot(111, projection="3d")
	# 
	# size = X[:, 3]
	# fill_colors = ['#FF9999' if v == 1 else '#FFE888' for v in labels]
	# edge_colors = ['red' if v == 1 else 'orange' for v in labels]
	# ax.scatter(X[:, 0], X[:, 1], X[:, 2], s=size, alpha=0.4, linewidths=X[:, 4], color=fill_colors, edgecolors=edge_colors)
	# 
	# plt.show()

test2()