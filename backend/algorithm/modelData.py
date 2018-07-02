import numpy as np
from sklearn.mixture import GaussianMixture as GMM 
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import linalg
import itertools
# just for importing models of django
import os
import sys
import django
sys.path.append("../..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from backendModels.models import User, QuantitativeLog

def startRun():
    quantitativeLogList = list(QuantitativeLog.objects.all().values_list('similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability',
        'sameArgsDiversity', 'webClassify'))
    # Generate random sample, two components
    np.random.seed(0)
    X = np.array(quantitativeLogList, dtype=np.float64)
    #min_max_scaler = preprocessing.MinMaxScaler()
    #X_minMax = min_max_scaler.fit_transform(X)
    X = preprocessing.scale(X)

    lowest_bic = np.infty
    bic = []
    n_components_range = range(2, 6)
    cv_types = ['spherical', 'tied', 'diag', 'full']
    # 协方差类型与分组个数的影响
    for cv_type in cv_types:
        for n_components in n_components_range:
            # Fit a Gaussian mixture with EM
            gmm = GMM(n_components=n_components, covariance_type=cv_type)
            gmm.fit(X)
            bic.append(gmm.bic(X))
            clf = gmm
            Y_ = clf.predict(X)
            if bic[-1] < lowest_bic:
                lowest_bic = bic[-1]
                best_gmm = gmm

    bic = np.array(bic)
    color_iter = itertools.cycle(['navy', 'turquoise', 'cornflowerblue', 'darkorange'])
    clf = best_gmm
    bars = []

    # Plot the BIC scores
    # 分成2X1,占用第一块
    temp = bic[3]
    bic[3] = bic[2]
    bic[2] = temp

    temp = bic[6]
    bic[6] = bic[7]
    bic[7] = temp

    temp = bic[10]
    bic[10] = bic[11]
    bic[11] = temp

    temp = bic[14]
    bic[14] = bic[15]
    bic[15] = temp

    spl = plt.subplot(2, 1, 1)
    hatches = ['o', '*', '.', '//']
    for i, (cv_type, color) in enumerate(zip(cv_types, color_iter)):
        xpos = np.array(n_components_range) + .2 * (i - 2)
        bars.append(plt.bar(xpos, bic[i * len(n_components_range):
                                    (i + 1) * len(n_components_range)],
                            width=.2, ec='black', ls="-", color='white',hatch=hatches[i]))
    # xticks:人为设置坐标轴的刻度显示的值
    plt.xticks(n_components_range)
    # ylim: 调整y轴范围
    plt.ylim([bic.min() * 1.01 - .01 * bic.max(), bic.max()])
    #plt.title('BIC score per model')
    xpos = np.mod(bic.argmin(), len(n_components_range)) + .65 +\
        .2 * np.floor(bic.argmin() / len(n_components_range))
    # text 在某位置添加文字
    plt.text(xpos + 0.9, bic.min() * 0.97 + .03 * bic.max(), '*', fontsize=14)
    spl.set_xlabel('Number of components')
    box = spl.get_position()
    #spl.set_position([box.x0, box.y0, box.width , box.height* 0.8])
    spl.legend([b[0] for b in bars], cv_types, bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.5)

    # Plot the winner
    #splot = plt.subplot(2, 1, 2)
    Y_ = clf.predict(X)
    res = {}
    for i in Y_:
        res[i] = res.get(i, 0) + 1
    print (Y_[35], Y_[89])
    print (Y_[95], Y_[174])
    print([k for k in res.keys()])
    print([v for v in res.values()])
    #for i, (mean, cov, color) in enumerate(zip(clf.means_, clf.covariances_, color_iter)):
    ##    # 求解矩阵特征方程
    ##    cov = cov.reshape((5, 5))
    ## 特征值,特征向量
    ##    w, u, v = linalg.svd(cov)
    #    v, w = linalg.eigh(cov)
    ##    # 矩阵Y_中是否有对应元素与i相等
    #    if not np.any(Y_ == i):
    #        continue
    ##    # 画离散点
    #    plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

    #    # Plot an ellipse to show the Gaussian component
    #    angle = np.arctan2(w[0][1], w[0][0])
    #    angle = 180. * angle / np.pi  # convert to degrees
    #    v = 2. * np.sqrt(2.) * np.sqrt(v)
    #    # 绘制椭圆
    #    ell = mpl.patches.Ellipse(mean, v[0], v[1], 180. + angle, color=color)
    #    ell.set_clip_box(splot.bbox)
    #    ell.set_alpha(.5)
    #    splot.add_artist(ell)

    #plt.xticks(())
    #plt.yticks(())
    #plt.title('Selected GMM: full model, 2 components')
    #plt.subplots_adjust(hspace=.35, bottom=.02)
    plt.show()