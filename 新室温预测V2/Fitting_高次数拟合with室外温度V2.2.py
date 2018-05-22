import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import datetime
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

def fit_func(K, inTemp_,retTemp_,heatingPower_,Temperature_outer_):
    # avg=(inTemp_+retTemp_)/2
    f1 = np.poly1d(K[0:3])
    f2 = np.poly1d(K[3:6])
    f3 = np.poly1d(K[6:9])
    f4 = np.poly1d(K[9:12])
    return f1(inTemp_) + f2(retTemp_) + f3(heatingPower_) + f4(Temperature_outer_)+ K[12]
    # return (inTemp_+retTemp_)/2-heatingPower_/K

def residuals_func(K, inTemp_,retTemp_,heatingPower_,Temperature_outer_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_,Temperature_outer_) - innerTemp_
    return ret


# print(inTemp[ind])
#2018-02-02 16:15:00
df["Timestamp"]=[datetime.datetime.strptime(m,"%Y-%m-%d %H:%M:%S") for m in df["Timestamp"]]
endTime=datetime.datetime.strptime("2018-2-10 0:0:0","%Y-%m-%d %H:%M:%S")
b2 = df["Timestamp"] < endTime
ind=df[b2].index         #获得2-10之前的数据

# 次卧预测温度
# K_init=np.random.rand(17)
# res=leastsq(residuals_func,K_init,args=(inTemp[ind],retTemp[ind],heatingPower[ind],Temperature_outer[ind],Temperature_bedroom[ind]))
#
# plt.figure()
# plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower,Temperature_outer),label="次卧预测温度")
# plt.plot(np.arange(l),Temperature_bedroom,"r",label="次卧真实温度")
# plt.ylim((10,22))
# plt.xlabel("#样例")
# plt.ylabel("温度(℃)")
# plt.title("四阶带室外温度(全数据)")
# plt.legend()
# plt.show()
#
#
# #书房预测温度
# K_init=np.random.rand(13)
# res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,Temperature_studyroom))
#
# plt.figure()
# plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower),label="书房预测温度")
# # print(fit_func(res[0], inTemp,retTemp,heatingPower)[:20])
# plt.plot(np.arange(l),Temperature_studyroom,"r",label="书房真实温度")
# plt.ylim((16,25))
# plt.xlabel("#样例")
# plt.ylabel("温度(℃)")
# plt.legend()
# plt.show()
#
#客厅北预测温度
# K_init=np.random.rand(17)
# res=leastsq(residuals_func,K_init,args=(inTemp[ind],retTemp[ind],heatingPower[ind],
#                                         Temperature_outer[ind],Temperature_sittingroomN[ind]))
# plt.figure()
# plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower,Temperature_outer),label="客厅北预测温度")
# plt.plot(np.arange(l),Temperature_sittingroomN,"r",label="客厅真实温度")
# # plt.ylim((10,22))
# plt.xlabel("#样例")
# plt.ylabel("温度(℃)")
# plt.title("四阶带室外温度(全数据)")
# plt.legend()
# plt.show()
#

#客厅南预测温度
K_init=np.random.rand(13)
res=leastsq(residuals_func,K_init,args=(inTemp[ind],retTemp[ind],heatingPower[ind],
                                        Temperature_outer[ind],Temperature_sittingroomS[ind]))

plt.figure()
plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower,Temperature_outer),label="客厅南预测温度")
plt.plot(np.arange(l),Temperature_sittingroomS,"r",label="客厅南真实温度")
plt.xlabel("#样例")
plt.ylabel("温度(℃)")
plt.title("三阶带室外温度")
plt.legend()
plt.show()

