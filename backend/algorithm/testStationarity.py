# _*_ coding:utf-8 _*_
# 宽平稳稳定性校验模块
from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# 移动平均图
def draw_trend(timeSeries, size):
    f = plt.figure(facecolor='white')
    # 对size个数据进行移动平均
    rol_mean = timeSeries.rolling(window=size).mean()
    # 对size个数据进行加权移动平均
    rol_weighted_mean = pd.ewma(timeSeries, span=size)

    timeSeries.plot(color='blue', label='Original')
    rol_mean.plot(color='red', label='Rolling Mean')
    rol_weighted_mean.plot(color='black', label='Weighted Rolling Mean')
    plt.legend(loc='best')
    plt.title('Rolling Mean')
    plt.show()

def draw_ts(timeSeries):
    timeSeries.plot(color='blue')
    plt.show()

# 单位根校验
# Test Statistic < Critical Value
# x: 序列，一维数组
# maxlag：差分次数
# regresion:{c:只有常量，
#            ct:有常量项和趋势项，
#            ctt:有常量项、线性和二次趋势项，
#            nc:无任何选项}
def testStationarity(ts):
    for maxlag in [1, 2, 3]:
        dftest = adfuller(ts, maxlag)
        # 对上述函数求得的值进行语义描述
        dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
        for key,value in dftest[4].items():
            if ((dftest[0] < value) or (dftest[1] < 0.05)):
                return True
    return False
    #for key,value in dftest[4].items():
    #    dfoutput['Critical Value (%s)'%key] = value
    #return dfoutput
