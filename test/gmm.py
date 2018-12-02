import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 构建示例数据集
from sklearn.datasets.samples_generator import make_blobs
X, y_true = make_blobs(n_samples=10000, centers=2, cluster_std=0.60, random_state=0, n_features=5)
# n_samples为样本个数，center表示产生数据的中心点，cluster_std表示数据集的标准差，random_state随机产生的结果与其值有关

# gmm
from sklearn.mixture import GaussianMixture as GMM
gmm = GMM(n_components=2).fit(X)
# covariance_type即通过EM算法估算参数时使用的协方差类型，默认full
labels = gmm.predict(X)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xs = X[:, 0]
ys = X[:, 1]
zs = X[:, 2]
data_points = [(x, y, z) for x, y, z in zip(xs, ys, zs)]

ss = X[:, 3]
colors = ['red' if v == 1 else 'yellow' for v in labels]

i = 0
for data, color, size in zip(data_points, colors, ss):
	i+=1
	x, y, z = data
	ax.scatter(x, y, z, c=color, s=size)
print (i)
plt.show()
