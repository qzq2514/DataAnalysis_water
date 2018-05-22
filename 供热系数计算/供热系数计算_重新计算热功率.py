import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

df=pd.read_excel("orgData.xls")
df_heatK=pd.read_excel("KValue.xlsx")

heatingPower=df.loc[:15,"瞬时热量(KW)"]
heatingFlow=df.loc[:15,"瞬时流量 (m³/h)"]
inTemp=df.loc[:15,"进水温度 (℃)"]
retTemp=df.loc[:15,"回水温度 (℃)"]
innerTemp=df.loc[:15,"室内温度(℃)"]

inTemp_int=round(inTemp).astype(int)
retTemp_int=round(retTemp).astype(int)
heatK = [k for k in map(lambda x,y:df_heatK.ix[50-x,y],retTemp_int,inTemp_int)] #得到不同温度对下的热系数

heatingPower=heatK*(inTemp-retTemp)*heatingFlow        #重新计算瞬时热量
# print(heatingPower)


def fit_func(K, inTemp_,retTemp_,heatingPower_):
    return (inTemp_+retTemp_)/2-heatingPower_/K

def residuals_func(K, inTemp_,retTemp_,heatingPower_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_) - innerTemp_
    return ret

K_init=np.random.rand(1)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,innerTemp))


plt.figure()
plt.plot(np.arange(16),fit_func(res[0], inTemp,retTemp,heatingPower),label="预测温度")
plt.plot(np.arange(16),innerTemp,"r",label="真实温度")
plt.xlabel("#样例")
plt.ylabel("室内温度(℃)")


plt.legend()
plt.show()

# print("供热系数:",float(res[0]))
