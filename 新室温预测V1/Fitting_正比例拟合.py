import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
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

# print(retTemp)
l=len(heatingPower)

def fit_func(K, inTemp_,retTemp_,heatingPower_):
    return (inTemp_+retTemp_)/2-heatingPower_/K

def residuals_func(K, inTemp_,retTemp_,heatingPower_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_) - innerTemp_
    return ret

#次卧预测温度
K_init=np.random.rand(1)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,Temperature_bedroom))

plt.figure()
plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower),label="次卧预测温度")
plt.plot(np.arange(l),Temperature_bedroom,"r",label="次卧真实温度")
plt.xlabel("#样例")
plt.ylabel("温度(℃)")
plt.legend()
plt.show()

#书房预测温度
K_init=np.random.rand(1)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,Temperature_studyroom))

plt.figure()
plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower),label="书房预测温度")
plt.plot(np.arange(l),Temperature_studyroom,"r",label="书房真实温度")
plt.xlabel("#样例")
plt.ylabel("温度(℃)")
plt.legend()
plt.show()

#客厅北预测温度
K_init=np.random.rand(1)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,Temperature_sittingroomN))

plt.figure()
plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower),label="客厅北预测温度")
plt.plot(np.arange(l),Temperature_sittingroomN,"r",label="客厅北真实温度")
plt.xlabel("#样例")
plt.ylabel("温度(℃)")
plt.legend()
plt.show()

#客厅南预测温度
K_init=np.random.rand(1)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,Temperature_sittingroomS))

plt.figure()
plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower),label="客厅南预测温度")
plt.plot(np.arange(l),Temperature_sittingroomS,"r",label="客厅南真实温度")
plt.xlabel("#样例")
plt.ylabel("温度(℃)")
plt.legend()
plt.show()

