import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
from mpl_toolkits.mplot3d import Axes3D

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="orgData.xls"
df=pd.read_excel(path)

inner=19

buInd=df['室外温度(℃)']>=6550
df.loc[buInd,'室外温度(℃)']=df.loc[buInd,'室外温度(℃)']-6553.6

#df.to_excel("outMy.xls",sheet_name="气候补偿数据")


#p为参数,对outTe,inTe均采用二次拟合
def fit_func(p, outTe,inTe):
    f_out=np.poly1d(p[0:6])
    f_in= np.poly1d(p[6])
    #f=p[0]*outTe**2+p[1]*outTe+p[2]*inTe**2+p[3]*inTe+p[4]
    return f_out(outTe)+f_in(inTe)+p[7]


# 损失函数
def residuals_func(p, y, outTe,inTe):
    ret = fit_func(p, outTe,inTe) - y
    return ret

p_init = np.random.randn(8)

res = leastsq(residuals_func, p_init, args=(df['二次供温(℃)'], df['室外温度(℃)'],df['室内温度(℃)']))
#print(res[0])        #res[0]是元素为拟合后的参数值集合

fig=plt.figure()
ax=Axes3D(fig)

X, Y = np.meshgrid(df['室外温度(℃)'][:20], df['室内温度(℃)'][:20])
value=fit_func(res[0],X,Y)
#print(Y)

print(value)
ax.plot_surface(X,Y,value,rstride=1, cstride=1, cmap='rainbow')

ax.set_zlabel('二次供温(℃)') #坐标轴
ax.set_ylabel('室内温度(℃)')
ax.set_xlabel('室外温度(℃)')
plt.show()