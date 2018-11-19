# numpy支持大量的维度数组与矩阵运算
import numpy as np
from sklearn.mixture import GaussianMixture as GMM 
from sklearn.cluster import KMeans
from sklearn import preprocessing
from scipy import linalg
import itertools
# import calDB
from sklearn.cluster import KMeans
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

def startRun():
    quantitativeLogList = list(QuantitativeLog.objects.all().values_list('similarEuc', 'urlArgsEntropy', 'abnormalTimeProbability',
        'sameArgsDiversity', 'webClassify'))

    # 数组元素的数据类型
    X = np.array(quantitativeLogList, dtype=np.float64)
    #min_max_scaler = preprocessing.MinMaxScaler()
    #X_minMax = min_max_scaler.fit_transform(X)
    #X = preprocessing.scale(X)

    # k均值聚类
    estimator = KMeans(n_clusters=2)#构造聚类器
    estimator.fit(X)#聚类
    label_pred = estimator.labels_ #获取聚类标签
    cluster1 = []
    cluster2 = []
    j = 0

    for i in label_pred:
        if (i == 1):
            cluster1.append(X[j][4])
        else:
            cluster2.append(-X[j][4])
        j += 1

    ##########  画图可选 ########
    # pltCharacter.plot(cluster1, cluster2, 'a')
    ##########  end     ########
    # Gmm model
    return
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
    bic[3] = bic[0]
    bic[0] = temp

    temp = bic[1]
    bic[1] = bic[2]
    bic[2] = temp

    temp = bic[7]
    bic[7] = bic[4]
    bic[4] = temp

    temp = bic[6]
    bic[6] = bic[5]
    bic[5] = temp

    temp = bic[12]
    bic[12] = bic[15]
    bic[15] = temp

    temp = bic[13]
    bic[13] = bic[14]
    bic[14] = temp

    spl = plt.subplot(2, 1, 1)
    hatches = ['o', '*', '.', '//']
    print(mpl.matplotlib_fname()) 
    mpl.rcParams['font.sans-serif']=['SimSun'] #指定默认字体 SimHei为黑体
    mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
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
    spl.set_xlabel('聚类数目')
    spl.set_ylabel('BIC分数')
    box = spl.get_position()
    #spl.set_position([box.x0, box.y0, box.width , box.height* 0.8])
    # ['球面协方差矩阵', '相同的完全协方差矩阵', '对角协方差矩阵', '完全协方差矩阵']
    spl.legend([b[0] for b in bars], ['球面协方差矩阵', '相同的完全协方差矩阵', '对角协方差矩阵', '完全协方差矩阵'], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.5)

    # Plot the winner
    #splot = plt.subplot(2, 1, 2)
    #Y_ = clf.predict(X)
    ##res = {}
    #cluster1 = []
    #cluster2 = []
    ## j = 0
    ## for i in Y_:
    ##     if (i == 0):
    ##         cluster1.append(X[j])
    ##     else:
    ##         cluster2.append(X[j])
    ##     j += 1
    ## print(calDB.dbi(np.array(cluster1), np.array(cluster2)))
    ## return
    ##    res[i] = res.get(i, 0) + 1
    ##print (Y_[35], Y_[89])
    ##print (Y_[95], Y_[174])
    ##print([k for k in res.keys()])
    ##print([v for v in res.values()])
    #for i, (mean, cov, color) in enumerate(zip(clf.means_, clf.covariances_, color_iter)):
    #    if (i==0):
    #        color = 'red'
    #    else:
    #        color = 'blue'
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

    #axes = plt.gca()
    #axes.set_xlim([-0.5,1.5])
    #axes.set_ylim([0,2])
    #plt.xticks(())
    #plt.yticks(())
    #plt.title('Selected GMM: full model, 2 components')
    plt.subplots_adjust(hspace=.35, bottom=.02)
    plt.show()