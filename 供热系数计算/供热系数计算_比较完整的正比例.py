import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import leastsq

#忽略一些无谓的警告
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#定义每层的结构
# def add_layer(input,in_size,out_size,active_function=None):
#     Weights=tf.Variable(tf.random_normal([out_size,in_size]))
#     biases=tf.Variable(tf.zeros([out_size,1])+0.1)
#
#     Wx_plus_b=tf.matmul(Weights,input) + biases
#
#     if active_function==None:
#         outputs=Wx_plus_b
#     else:
#         outputs = active_function(Wx_plus_b)
#     return outputs

path="orgData.xls"
df=pd.read_excel(path)

heatingPower=np.array(df.loc[:15,"瞬时热量(KW)"])
inTemp=df.loc[:15,"进水温度 (℃)"]
retTemp=df.loc[:15,"回水温度 (℃)"]
innerTemp=df.loc[:15,"室内温度(℃)"]

inputData=np.array((inTemp+retTemp)/2-innerTemp)

# print(inputData.shape)

# heatingPower=np.matrix(heatingPower).getA()  #将(16,)维度转为为(1,16)
# inputData=np.matrix(inputData).getA()

# inTemp=np.matrix(inTemp).getA()
# retTemp=np.matrix(retTemp).getA()
# innerTemp=np.matrix(innerTemp).getA()
#
# print(heatingPower.shape)
#
# K=tf.Variable(0.13)
# #
x_data=inputData              #(进水温度+回水温度)/2－室内温度　　作为数据的X
y_data=heatingPower           #直接将供热功率作为数据的Y,即标签

plt.figure()
plt.scatter(x_data,y_data)  #画出图

def fit_func(K, x_data_):
    return x_data_*K    #定义关系式，原本给定的关系是正比例:y_data=x_data_*K,求出合适的K

def residuals_func(K, x_data_,y_data_):
    ret = fit_func(K, x_data_) - y_data_   #定义损失
    return ret


K_init=np.random.randn(1)

# x_data=np.array(x_data)
# print(x_data.shape)
res=leastsq(residuals_func,K_init,args=(x_data,y_data))

print("供热系数K:",float(res[0]))   #0.12558476771384813

plt.plot(x_data,fit_func(float(res[0]),x_data),"r-")   #画出预测值
plt.show()