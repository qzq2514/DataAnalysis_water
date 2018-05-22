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

def fit_func(K,avg,heatingPower_):
    f1 = np.poly1d(K[0:4])
    f2 = np.poly1d(K[4:8])
    return f1(avg) + f2(heatingPower_) + K[8]

def residuals_func(K, avg,heatingPower_,innerTemp_):
    ret = fit_func(K, avg,heatingPower_) - innerTemp_
    return ret


# print(inTemp[ind])
#2018-02-02 16:15:00
df["Timestamp"]=[datetime.datetime.strptime(m,"%Y-%m-%d %H:%M:%S") for m in df["Timestamp"]]
endTime=datetime.datetime.strptime("2018-2-10 0:0:0","%Y-%m-%d %H:%M:%S")
b2 = df["Timestamp"] < endTime
ind=df[b2].index         #获得2-10之前的数据

#客厅南预测温度

#参数拟合
K_init=np.random.rand(9)
res=leastsq(residuals_func,K_init,args=((inTemp[ind]+retTemp[ind])/2,heatingPower[ind],Temperature_sittingroomS[ind]))

fig=plt.figure()
ax=Axes3D(fig)
[X,Y]= np.meshgrid((inTemp[:50]+retTemp[:50])/2,heatingPower[:50])
value=fit_func(res[0],X,Y)

print(value)
pls=ax.plot_surface(X,Y,value,rstride=1, cstride=1, cmap='rainbow')
plt.colorbar(pls)
ax.set_xlabel('供回水平均(℃)')
ax.set_ylabel('功率(kw)')
ax.set_zlabel('客厅南温度预测(℃)') #坐标轴

plt.show()


