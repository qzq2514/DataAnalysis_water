import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.mplot3d import Axes3D
#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="orgData.xls"
df=pd.read_excel(path)

heatingPower=df["Power (kW)"]
inTemp=df["Flow temperature (°C)"]
retTemp=df["Return temperature (°C)"]
Temperature_bedroom=df["Temperature_bedroom(°C)"]
Temperature_studyroom=df["Temperature_studyroom(°C)"]
Temperature_sittingroomN=df["Temperature_sittingroomN(°C)"]
Temperature_sittingroomS=df["Temperature_sittingroomS(°C)"]
Temperature_outer=df["Temperature_outer(°C)"]

# print(retTemp)
l=len(heatingPower)

def fit_func(K, inTemp_,retTemp_,heatingPower_):
    f1 = np.poly1d(K[0:4])
    f2 = np.poly1d(K[4:8])
    f3 = np.poly1d(K[8:12])
    return f1(inTemp_) +f2(retTemp_) +f3(heatingPower_) + K[12]

def residuals_func(K, inTemp_,retTemp_,heatingPower_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_) - innerTemp_
    return ret


# print(inTemp[ind])
#2018-02-02 16:15:00
df["Timestamp"]=[datetime.datetime.strptime(m,"%Y-%m-%d %H:%M:%S") for m in df["Timestamp"]]
endTime=datetime.datetime.strptime("2018-2-10 0:0:0","%Y-%m-%d %H:%M:%S")
b2 = df["Timestamp"] < endTime
ind=df[b2].index         #获得2-10之前的数据

#客厅南预测温度

#参数拟合
K_init=np.random.rand(13)
res=leastsq(residuals_func,K_init,args=(inTemp[ind],retTemp[ind],heatingPower[ind],Temperature_sittingroomS[ind]))

fig=plt.figure()
ax=Axes3D(fig)
value=fit_func(res[0], inTemp,retTemp,heatingPower)  #获得预测室温

#补充图plot_trisurf并不能实现四维的效果
#本来想着ax.plot_trisurf(inTemp, retTemp, heatingPower,c=value,cmap=plt.cm.hot)  谁知没有c属性
ax.plot_trisurf(inTemp, retTemp, heatingPower,cmap=plt.cm.hot)
ax.set_xlabel('供水温度(℃)')
ax.set_ylabel('回水温度(℃)')
ax.set_zlabel('功率(kw') #坐标轴
plt.show()
