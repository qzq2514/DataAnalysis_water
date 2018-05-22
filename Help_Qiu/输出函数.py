import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False


path="dataT.xls"
df=pd.read_excel(path)

heatingPower=df["Power (kW)"]
inTemp=df["Flow temperature (°C)"]
retTemp=df["Return temperature (°C)"]
Temperature_bedroom=df["Temperature_bedroom(°C)"]
Temperature_studyroom=df["Temperature_studyroom(°C)"]
Temperature_sittingroomN=df["Temperature_sittingroomN(°C)"]
Temperature_sittingroomS=df["Temperature_sittingroomS(°C)"]
Temperature_Outside=df["Temperature_outer(°C)"]

# print(retTemp)
l=len(heatingPower)

def fit_func(K, inTemp_,innerTemp_):
    #改变这里的3系数，可以改变曲线的曲率
    f1 = np.poly1d(K[0:3])
    return K[3]*np.power(inTemp_,3) + f1(innerTemp_)+ K[5]

def residuals_func(K, inTemp_,innerTemp_,Temperature_Outside_):
    ret = fit_func(K, inTemp_,innerTemp_) - Temperature_Outside_
    return ret


#客厅北预测温度
K_init=np.random.rand(6)
res=leastsq(residuals_func,K_init,args=(inTemp,Temperature_sittingroomS,Temperature_Outside))
# print(res[0])

t_gong=np.linspace(30,60,50)
y_outer=fit_func(res[0],t_gong,20)
plt.plot(t_gong,y_outer)
plt.ylim(-15,15)
plt.xlabel("供水温度")
plt.ylabel("室外温度")
plt.show()
