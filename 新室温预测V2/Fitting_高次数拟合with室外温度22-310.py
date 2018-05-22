import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

#2.2日-3.10日的数据直接data22-310.xls,不用getNewTable
path="data22-310.xls"
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

def fit_func(K, inTemp_,retTemp_,heatingPower_,Temperature_outer_):
    #avg=(inTemp_+retTemp_)/2
    f1 = np.poly1d(K[0:2])
    f2 = np.poly1d(K[2:4])
    f3 = np.poly1d(K[4:9])
    f4 = np.poly1d(K[9:14])
    return f1(inTemp_) +f2(retTemp_)+ f3(heatingPower_)+f4(Temperature_outer_) + K[14]

def residuals_func(K, inTemp_,retTemp_,heatingPower_,Temperature_outer_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_,Temperature_outer_) - innerTemp_
    return ret



lstTime=[datetime.datetime.strptime(m,"%Y-%m-%d %H:%M:%S") for m in df["Timestamp"]]
df["Timestamp"]=lstTime
endTime=datetime.datetime.strptime("2018-3-1 0:0:0","%Y-%m-%d %H:%M:%S")
b2 = df["Timestamp"] < endTime
ind=df[b2].index       #获得2-10之前的数据


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
K_init=np.random.rand(15)
res=leastsq(residuals_func,K_init,args=(inTemp[ind],retTemp[ind],heatingPower[ind],
                                        Temperature_outer[ind],Temperature_sittingroomS[ind]))

pred=fit_func(res[0], inTemp,retTemp,heatingPower,Temperature_outer)


# bb=Temperature_sittingroomS.index%3==0   #每隔5个数去一个温度
# ind=Temperature_sittingroomS[bb].index
#
# Temperature_sittingroomS=Temperature_sittingroomS[ind]
# # print(Temperature_sittingroomS.index)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M:%S"))
print(type(lstTime))
plt.plot(lstTime, pred,label="客厅南预测温度")
plt.plot(lstTime, Temperature_sittingroomS,"r",label="客厅南真实温度")
plt.gcf().autofmt_xdate()
plt.xlabel("时间")
plt.ylabel("温度(℃)")
plt.legend()
plt.show()