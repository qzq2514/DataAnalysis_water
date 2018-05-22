import numpy as np
import pandas as pd
from scipy.optimize import leastsq
path="orgData.xls"
df=pd.read_excel(path)

heatingPower=df.loc[:15,"瞬时热量(KW)"]
inTemp=df.loc[:15,"进水温度 (℃)"]
retTemp=df.loc[:15,"回水温度 (℃)"]
innerTemp=df.loc[:15,"室内温度(℃)"]
# print(retTemp)

def fit_func(K, inTemp_,retTemp_,innerTemp_):
    return K*((inTemp_+retTemp_)/2-innerTemp_)

def residuals_func(K, heatingPower_, inTemp_,retTemp_,innerTemp_):
    ret = np.mean(np.square(fit_func(K, inTemp_,retTemp_,innerTemp_) - heatingPower_))
    # ret = fit_func(K, inTemp_, retTemp_, innerTemp_) - heatingPower_
    return ret

K_init=np.random.randn(1)
res=leastsq(residuals_func,K_init,args=(heatingPower,inTemp,retTemp,innerTemp))

print("供热系数KK:",float(res[0]))   #0.12558476716707778
# print(fit_func(res[0],inTemp,retTemp,innerTemp))
val=(inTemp+retTemp)/2-innerTemp
# print(val)
# print("--------------")
# print(heatingPower)
print(heatingPower/val)