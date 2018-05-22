import numpy as np
import pandas as pd
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="orgData.xls"
df=pd.read_excel(path)

heatingPower=df.loc[:15,"瞬时热量(KW)"]
inTemp=df.loc[:15,"进水温度 (℃)"]
retTemp=df.loc[:15,"回水温度 (℃)"]
innerTemp=df.loc[:15,"室内温度(℃)"]
# print(retTemp)

def fit_func(K, inTemp_,retTemp_,heatingPower_):
    return (inTemp_+retTemp_)/2-heatingPower_/K

def residuals_func(K, inTemp_,retTemp_,heatingPower_,innerTemp_):
    ret = fit_func(K, inTemp_,retTemp_,heatingPower_) - innerTemp_
    # ret = fit_func(K, inTemp_, retTemp_, innerTemp_) - heatingPower_
    return ret

K_init=np.random.rand(1)
res=leastsq(residuals_func,K_init,args=(inTemp,retTemp,heatingPower,innerTemp))

# print(residuals_func(res[0], inTemp,retTemp,heatingPower,innerTemp))

plt.figure()
plt.plot(np.arange(16),fit_func(res[0], inTemp,retTemp,heatingPower),label="预测温度")
plt.plot(np.arange(16),innerTemp,"r",label="真实温度")
plt.xlabel("#样例")
plt.ylabel("室内温度(℃)")

print()
# print(fit_func(res[0], inTemp,retTemp,heatingPower))
plt.legend()
plt.show()
# print(K_init)
# print("供热系数Kk:",float(res[0]))
# print(fit_func(res[0],inTemp,retTemp,innerTemp))

