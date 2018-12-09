import matplotlib.pyplot as plt
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
