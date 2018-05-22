import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.mplot3d import Axes3D
#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="data.xls"
df=pd.read_excel(path)

heatingPower=df["Power (kW)"]
inTemp=df["Flow temperature (°C)"]
retTemp=df["Return temperature (°C)"]
Temperature_sittingroomS=df["Temperature_sittingroomS(°C)"]

# print(retTemp)
l=len(heatingPower)

def fit_func(K,inTemp_,retTemp_,innerTemp_):
    f1 = np.poly1d(K[0:4])
    f2 = np.poly1d(K[4:8])
    f3 = np.poly1d(K[8:12])
    # return K*((inTemp_+retTemp_)/2-innerTemp_)  #使用之前的正比例关系拟合
    return f1(inTemp_) + f2(retTemp_) + f3(innerTemp_)+K[12]

def residuals_func(K, inTemp_,retTemp_,innerTemp_,heatingPower_):
    ret = fit_func(K, inTemp_,retTemp_,innerTemp_) - heatingPower_
    return ret


#参数拟合
K_init=np.random.rand(13)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,Temperature_sittingroomS,heatingPower))

fig=plt.figure()
ax=Axes3D(fig)
[X,Y]= np.meshgrid(inTemp[:15],retTemp[:15])
for t in range(18,24):
    value=fit_func(res[0],X,Y,t)   #20度室内温度
    ax1=ax.plot_surface(X,Y,value,rstride=1, cstride=1)

ax.set_xlabel('供水温度(℃)')
ax.set_ylabel('回水温度(℃)')
ax.set_zlabel('功率(kw)') #坐标轴
plt.show()


