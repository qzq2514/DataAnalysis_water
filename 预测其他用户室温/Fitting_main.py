import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
import datetime
#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="data/standardData.xls"
df=pd.read_excel(path)

heatingPower=df["Power (kW)"]
inTemp=df["Flow temperature (°C)"]
retTemp=df["Return temperature (°C)"]
Temperature_sittingroomS=df["Temperature_sittingroomS(°C)"]

def fit_func(K, inTemp_,retTemp_,heatingPower_):
    f1 = np.poly1d(K[0:2])
    f2 = np.poly1d(K[2:4])
    f3 = np.poly1d(K[4:8])
    return f1(inTemp_) + f2(retTemp_) + f3(heatingPower_) + K[8]
    # return (heatingPower_-K * ((inTemp_ + retTemp_) / 2))

def residuals_func(K, inTemp_,retTemp_,heatingPower_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_) - innerTemp_
    return ret

# df["Timestamp"]=[datetime.datetime.strptime(m,"%Y-%m-%d %H:%M:%S") for m in df["Timestamp"]]
# endTime=datetime.datetime.strptime("2018-2-10 0:0:0","%Y-%m-%d %H:%M:%S")
# b2 = df["Timestamp"] < endTime
# ind=df[b2].index         #获得2-10之前的数据

#使用郭家数据进行拟合客厅南预测温度
K_init=np.random.rand(9)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,Temperature_sittingroomS))

#画出郭家的预测图
plt.figure()
l=len(df)
plt.plot(np.arange(l),fit_func(res[0], inTemp,retTemp,heatingPower),label="客厅南预测温度")
plt.plot(np.arange(l),Temperature_sittingroomS,"r",label="客厅南真实温度")
plt.xlabel("#样例")
plt.ylabel("温度(℃)")
plt.title("郭家室温预测")
plt.legend()
plt.show()

#
name=["4-1-2001","5-1-1003","5-1-2401"]
for n in range(3):
    path = "data/data%d.xls"% (n+1)
    print(path)
    df = pd.read_excel(path)

    heatingPower = df["Power (kW)"]
    inTemp = df["Flow temperature (°C)"]
    retTemp = df["Return temperature (°C)"]
    Temperature_sittingroomS = df["Temperature_sittingroomS(°C)"]

    l = len(df)
    plt.plot(np.arange(l), fit_func(res[0], inTemp, retTemp, heatingPower), label="客厅南预测温度")
    plt.plot(np.arange(l), Temperature_sittingroomS, "r", label="客厅南真实温度")
    plt.xlabel("#样例")
    plt.ylabel("温度(℃)")
    plt.title("%s用户室温预测"%name[n])
    plt.legend()
    plt.show()

