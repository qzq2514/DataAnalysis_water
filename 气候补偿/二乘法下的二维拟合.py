import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="orgData.xls"
df=pd.read_excel(path)

inner=20

buInd=df['室外温度(℃)']>=6550
df.loc[buInd,'室外温度(℃)']=df.loc[buInd,'室外温度(℃)']-6553.6

#df.to_excel("outMy.xls", sheet_name="气候补偿数据")
df=df.sort_values(by='室外温度(℃)')


def fit_func(p, outTe,inTe):
    f_out=np.poly1d(p[0:5])
    f_in= np.poly1d(p[6:8])
    #f=p[0]*outTe**2+p[1]*outTe+p[2]*inTe**2+p[3]*inTe+p[4]
    return f_out(outTe)+f_in(inTe)+p[8]


# 损失函数
def residuals_func(p, y, outTe,inTe):
    ret = fit_func(p, outTe,inTe) - y
    return ret

p_init = np.random.randn(9)

res = leastsq(residuals_func, p_init, args=(df['二次供温(℃)'], df['室外温度(℃)'],df['室内温度(℃)']))
#print(res[0])        #res[0]是元素为拟合后的参数值集合


# plt.scatter(df['室外温度(℃)'],df['二次供温(℃)'])
yvalue=fit_func(res[0],df['室外温度(℃)'],inner)
plt.plot(df['室外温度(℃)'],yvalue,'b-')
plt.xlabel('室外温度(℃)')                #增加轴名
plt.ylabel('供水温度(℃)')

#plt.xlim((-1,2))         #设置x,y轴的显示区域
plt.ylim((np.min(yvalue)-0.1,np.max(yvalue)+0.1))
plt.text(df['室外温度(℃)'][100], yvalue[100]-1, "室外温度%s(℃)时的曲线" % inner)
plt.show()