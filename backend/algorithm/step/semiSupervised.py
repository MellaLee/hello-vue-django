import copy as cp
import numpy as np
from scipy import optimize
from scipy import sparse
import time

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc  ###计算roc和auc
import matplotlib as mpl
from sklearn import preprocessing
from scipy import interp
from sklearn.model_selection import StratifiedKFold

# just for importing models of django
import os
import sys
import django
import random
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog

mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

class linear_k:

	def __init__(self, issparse):
		self._sparse = issparse

	def compute(self, data1, data2):
		if self._sparse:
			return data1 * data2.T
		else:
			return np.mat(data1) * np.mat(data2).T

class rbf_k:

	def __init__(self, sigma, issparse):
		self._sparse = issparse
		self._sigma = sigma

	def compute(self, mat1, mat2):
		mat1 = np.mat(mat1)
		mat2 = np.mat(mat2)
		mat1T_mat1 = np.mat([(v * v.T)[0, 0] for v in mat1]).T
		mat2T_mat2 = np.mat([(v * v.T)[0, 0] for v in mat2]).T
		mat1T_mat1 = mat1T_mat1 * np.mat(np.ones((mat2.shape[0], 1), dtype=np.float64)).T
		mat2T_mat2 = np.mat(np.ones((mat1.shape[0], 1), dtype=np.float64)) * mat2T_mat2.T
		k = mat1T_mat1 + mat2T_mat2
		k -= 2 * mat1 * mat2.T
		k *= - 1. / (2 * np.power(self._sigma, 2))
		return np.exp(k)

class Quasi_Newton_S3VM:

	def __init__(self, X_l, y, X_u, class_ratio=-1., lam=1., lam_u=1.,
				 sigma=1., kernel="rbf", s=3., gamma=20.):
		print ("initialization")
		self._start = time.time()
		self._X_l = X_l
		self._X_u = X_u
		self._y_T = np.mat(y, dtype=np.float64).T
		self._size_labeled = X_l.shape[0]
		self._size_unlabeled = X_u.shape[0]
		print (X_l.shape[0], X_u.shape[0])
		self._size_total = self._size_labeled + self._size_unlabeled
		self._lam = lam
		self._lam_u = lam_u
		self._sigma = sigma
		self._kernel = kernel
		self._gamma = gamma
		self._s = s
		if class_ratio == -1.:
			self._b = (1. / y.shape[0]) * np.sum(y)
		else:
			self._b = 2*class_ratio - 1
		self._numerically_stable_threshold = 500
		if sparse.issparse(self._X_l) and sparse.issparse(self._X_u):
			self._sparse = True
			self._X = sparse.vstack((X_l, X_u))
			self._X_u_mean = self._X_u.mean(axis=0)
			self._X_u_T = X_u.T
			self._X_l_T = X_l.T
			self._X_T = self._X.T
		else:
			print ("computing kernel")
			self._sparse = False
			self._X = np.vstack((X_l, X_u))
			if self._kernel == "linear":
				self._kernel = linear_k(self._sparse)
			elif self._kernel == "rbf":
				self._kernel = rbf_k(self._sigma, self._sparse)
			self._K_l = self._kernel.compute(self._X_l, self._X)
			self._K_u = self._kernel.compute(self._X_u, self._X)
			if self._sparse:
				self._K_m_tmp = sparse.bmat([[self._K_l], [self._K_u]])
			else:
				self._K_m_tmp = np.bmat([[self._K_l], [self._K_u]])
			self._K_m = self._K_m_tmp
			self._center_kernel()

	def _center_kernel(self):
		print ("centering kernel")
		self._K_X_X_u = self._kernel.compute(self._X, self._X_u)
		self._K_X_X_u_or_mean = (1. / self._size_unlabeled) * self._K_X_X_u.sum(axis=1)
		self._K_X_u_X = self._kernel.compute(self._X_u, self._X)
		self._K_X_u_X_ve_mean = (1. / self._size_unlabeled) * self._K_X_u_X.sum(axis=0)
		self._K_X_u_X_u = self._kernel.compute(self._X_u, self._X_u)
		self._K_X_u_X_u_mean = (1. / self._size_unlabeled ** 2) * self._K_X_u_X_u.sum()
		self._K_m_tmp = self._K_m_tmp - self._K_X_X_u_or_mean - \
						self._K_X_u_X_ve_mean + self._K_X_u_X_u_mean
		self._K_m = self._K_m_tmp
		self._K_l = self._K_m_tmp[range(0, self._size_labeled), :]
		print (self._K_m_tmp, self._size_labeled, self._size_total)
		self._K_u = self._K_m_tmp[range(self._size_labeled, self._size_total), :]

	def fit(self):
		print ("training started")
		self._annealing()

	def get_predictions(self, X, decision_function=False):
		print ("predicting")
		if self._sparse:
			W = self._X.T * self._c - self._X_u_mean.T * np.sum(self._c)
			predictions = (X * W + self._b).T
		else:
			K_X_t_X = self._kernel.compute(X, self._X)
			K_X_t_X_u = self._kernel.compute(X, self._X_u)
			K_X_t_X_u_or_mean = (1.0 / self._size_unlabeled) * K_X_t_X_u.sum(axis=1)
			K_X_t_X = K_X_t_X - K_X_t_X_u_or_mean - self._K_X_u_X_ve_mean + self._K_X_u_X_u_mean
			predictions = (K_X_t_X * self._c + self._b).T
		if decision_function is True:
			return predictions.tolist()[0]
		else:
			return np.sign(predictions).tolist()[0]

	def get_train_time(self):
		return self._train_time

	def _annealing(self):
		c_current = np.zeros(self._size_total, dtype=np.float64)
		for i in [float(self._lam_u*i) for i in [.0, 0.000001, 0.0001, 0.01, 0.1, 0.5, 1.]]:
			print ("annealing with lam_u =", i)
			self._lam_u = i
			c_current = self._bfgs(c_current)
		self._c = np.mat(c_current).T
		self._train_time = time.time() - self._start

	def _bfgs(self, c):
		if self._sparse:
			return optimize.fmin_l_bfgs_b(self._objective_function_sparse, c, m=50,
									  fprime=self._objective_function_gradient_sparse, maxfun=500,
									  factr=488288000, pgtol=1.0000000000000001e-05, iprint=-1)[0]
		else:
			return optimize.fmin_l_bfgs_b(self._objective_function, c, m=50,
									  fprime=self._objective_function_gradient, maxfun=500,
									  factr=488288000, pgtol=1.0000000000000001e-05, iprint=-1)[0]

	def _objective_function(self, c):
		#start = time.time()
		c = np.mat(c).T
		labeled_loss_tmp = self._gamma*(1. - np.multiply(self._y_T, self._K_l * c + self._b))
		labeled_loss_stable = cp.deepcopy(labeled_loss_tmp)
		mask = labeled_loss_tmp > 1./self._numerically_stable_threshold
		labeled_loss_stable[mask] = 0
		labeled_loss = np.log(1. + np.exp(labeled_loss_stable))
		np.place(labeled_loss, mask, np.array(labeled_loss_tmp[mask])[0])
		labeled_loss = (1./(self._gamma*self._size_labeled)) * np.sum(labeled_loss)
		unlabeled_loss = self._K_u * c + self._b
		unlabeled_loss = np.multiply(unlabeled_loss, unlabeled_loss)
		unlabeled_loss = (self._lam_u / self._size_unlabeled) * np.sum(np.exp(-self._s * unlabeled_loss))
		margin = self._lam * (c.T * self._K_m * c)
		#print "time for objective function", time.time() - start
		return labeled_loss + unlabeled_loss + margin

	def _objective_function_gradient(self, c):
		#start = time.time()
		c = np.mat(c).T
		a_labeled_tmp = self._gamma * (1. - np.multiply(self._y_T, self._K_l * c + self._b))
		a_labeled_stable = cp.deepcopy(a_labeled_tmp)
		mask = a_labeled_tmp > 1./self._numerically_stable_threshold
		a_labeled_stable[mask] = 0
		a_labeled = np.exp(a_labeled_stable)
		a_labeled = np.multiply(a_labeled, 1./(1. + a_labeled))
		a_labeled[mask] = 1
		a_labeled = (-1./self._size_labeled) * np.multiply(self._y_T, a_labeled)
		k_a_labeled = a_labeled.T * self._K_l
		a_unlabeled_tmp = (self._K_u * c + self._b)
		a_unlabeled = np.multiply(a_unlabeled_tmp, a_unlabeled_tmp)
		a_unlabeled = np.exp(-self._s * a_unlabeled)
		a_unlabeled = (-2. * self._s * self._lam_u / self._size_unlabeled) \
					  * np.multiply(a_unlabeled, a_unlabeled_tmp)
		k_a_unlabeled = a_unlabeled.T * self._K_u
		margin = (2. * self._lam * (self._K_m * c)).T
		#print "time for objective function gradient", time.time() - start
		return (k_a_labeled + k_a_unlabeled + margin).T

	def _objective_function_sparse(self, c):
		c = np.mat(c).T
		c_sum = np.sum(c)
		X_t_c = self._X_T*c - self._X_u_mean.T * c_sum
		labeled_loss_tmp = self._gamma*(1.0 - np.multiply(self._y_T,
														  (self._X_l * X_t_c - self._X_u_mean * X_t_c) + self._b))
		labeled_loss_stable = cp.deepcopy(labeled_loss_tmp)
		mask = labeled_loss_tmp > 1./self._numerically_stable_threshold
		labeled_loss_stable[mask] = 0
		labeled_loss = np.log(1. + np.exp(labeled_loss_stable))
		np.place(labeled_loss, mask, np.array(labeled_loss_tmp[mask])[0])
		labeled_loss = (1./(self._gamma*self._size_labeled)) * np.sum(labeled_loss)
		unlabeled_loss = (self._X_u * X_t_c - self._X_u_mean * X_t_c) + self._b
		unlabeled_loss = np.multiply(unlabeled_loss, unlabeled_loss)
		unlabeled_loss = (self._lam_u/self._size_unlabeled)*np.sum(np.exp(-self._s * unlabeled_loss))
		margin = self._lam * c.T * (self._X * X_t_c - self._X_u_mean * X_t_c)
		return labeled_loss + unlabeled_loss + margin

	def _objective_function_gradient_sparse(self, c):
		c = np.mat(c).T
		c_sum = np.sum(c)
		XTc = self._X_T * c - self._X_u_mean.T * c_sum
		a_labeled_tmp = self._gamma*(1.0 - np.multiply(self._y_T,
													   (self._X_l * XTc - self._X_u_mean * XTc) + self._b))
		a_labeled_stable = cp.deepcopy(a_labeled_tmp)
		mask = a_labeled_tmp > 1./self._numerically_stable_threshold
		a_labeled_stable[mask] = 0
		a_labeled = np.exp(a_labeled_stable)
		a_labeled = np.multiply(a_labeled, 1./(1. + a_labeled))
		a_labeled[mask] = 1
		a_labeled = np.multiply(self._y_T, a_labeled)
		a_labeled = self._X_l_T * a_labeled - self._X_u_mean.T * np.sum(a_labeled)
		K_a_labeled = (-1./self._size_labeled) * (self._X * a_labeled - self._X_u_mean * a_labeled)
		a_unlabeled_tmp = (self._X_u * XTc - self._X_u_mean * XTc) + self._b
		a_unlabeled = np.multiply(a_unlabeled_tmp, a_unlabeled_tmp)
		a_unlabeled = np.exp(-self._s * a_unlabeled)
		a_unlabeled = np.multiply(a_unlabeled, a_unlabeled_tmp)
		a_unlabeled = self._X_u_T * a_unlabeled - self._X_u_mean.T * np.sum(a_unlabeled)
		K_a_unlabeled = ((-2. * self._s * self._lam_u)/self._size_unlabeled) *\
						(self._X * a_unlabeled - self._X_u_mean * a_unlabeled)
		margin = 2.*self._lam*(self._X * XTc - self._X_u_mean * XTc)
		return (K_a_labeled + K_a_unlabeled + margin).T

def startRun():
	# fetch data
	X_cluster, Y_cluster = fetchClusterData()
	
	# 标准化数据 
	X_cluster = np.array(X_cluster, dtype=np.float64)
	Y_cluster = np.array(Y_cluster, dtype=np.float64)
	for index, x in enumerate(X_cluster):
		X_cluster[index] = preprocessing.scale(x)

	# 拆分数据
	skf = StratifiedKFold(n_splits=10)
	
	mean_tpr = 0.0
	mean_fpr = np.linspace(0, 1, logTotal)
	threshold = 0.0
	i=0

	for train, test in skf.split(X_cluster, Y_cluster):
		i+=1
		cv = StratifiedKFold(n_splits=2)
		X_train = X_cluster[train]
		Y_train = Y_cluster[train]
		for unlabel, label in cv.split(X_train, Y_train):
			break
		s3vm = Quasi_Newton_S3VM(X_train[label], Y_train[label], X_train[unlabel])
		s3vm.fit()
		y_score = s3vm.get_predictions(X_cluster[test], True)
		fpr,tpr,thresholds = roc_curve(Y_cluster[test], y_score) ###计算真正率和假正率
		optimal_idx = np.argmax(np.abs(tpr - fpr))
		optimal_threshold = thresholds[optimal_idx]
		threshold += optimal_threshold

		roc_auc = auc(fpr,tpr) ###计算auc的值
		mean_tpr += interp(mean_fpr, fpr, tpr)			#对mean_tpr在mean_fpr处进行插值，通过scipy包调用interp()函数
		mean_tpr[0] = 0.0
		plt.plot(fpr/7, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))

	mean_tpr /= 10 					#在mean_fpr100个点，每个点处插值插值多次取平均
	threshold /= 10 					#在mean_fpr100个点，每个点处插值插值多次取平均
	mean_tpr[-1] = 1.0 						#坐标最后一个点为（1,1）
	mean_auc = auc(mean_fpr, mean_tpr)		#计算平均AUC值
	#画平均ROC曲线
	#print mean_fpr,len(mean_fpr)
	#print mean_tpr
	plt.plot(mean_fpr/7, mean_tpr, 'k--',
			label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)
	
	#画对角线
	plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
	# optimal_idx = np.argmax(np.abs(mean_tpr - mean_fpr))
	# plt.scatter(mean_fpr[optimal_idx], mean_tpr[optimal_idx], s=80, c='r', marker=(9,2,30), alpha=0.5)
	# x = np.float64(mean_fpr[optimal_idx]).item()
	# y = np.float64(mean_tpr[optimal_idx]).item()
	# plt.text(x, y,"(" + str(round(x, 3)) + "," + str(round(y, 3)) + ")",fontdict={'size':'16','color':'r'})
	print(threshold)
	plt.xlim([0.0, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('假阳性率')
	plt.ylabel('真阳性率')
	plt.legend(loc="lower right")
	print (time.strftime('%H.%M.%S',time.localtime(time.time())))
	plt.show()

# 黑样本有5000个
# 白样本有20000个
def fetchClusterData():
	goodlog = QuantitativeLog.objects.filter(label=0).all()[:logTotal * gr]
	badlog = QuantitativeLog.objects.filter(label=1).all()[:logTotal * br]

	X_goodlog = [list(x) for x in goodlog.values_list('similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability', 'sameArgsDiversity', 'webClassify')]
	Y_goodlog =[x[0] for x in goodlog.values_list('label')]
	# id_goodlog = [x[0] for x in goodlog.values_list('id')] 

	X_badlog = [list(x) for x in badlog.values_list('similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability', 'sameArgsDiversity', 'webClassify')]
	Y_badlog = [x[0] for x in badlog.values_list('label')]
	# id_badlog = [x[0] for x in badlog.values_list('id')] 

	X_cluster = X_goodlog + X_badlog
	Y_cluster = Y_goodlog + Y_badlog
	# id_log = id_goodlog[:each_type_num] + id_badlog[:each_type_num]
	# return X_cluster, Y_cluster, id_log
	return X_cluster, Y_cluster

logTotal = 15000 
gr = 0.8 
br = 0.2 
if __name__ == "__main__":
	startRun()

