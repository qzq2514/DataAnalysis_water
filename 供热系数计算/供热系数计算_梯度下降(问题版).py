import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import leastsq

#忽略一些无谓的警告
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def add_layer(input,in_size,out_size,active_function=None):
    Weights=tf.Variable(tf.random_normal([out_size,in_size]))
    biases=tf.Variable(tf.zeros([out_size,1])+0.1)

    Wx_plus_b=tf.matmul(Weights,input) + biases

    if active_function==None:
        outputs=Wx_plus_b
    else:
        outputs = active_function(Wx_plus_b)
    return outputs


#1.用下面的数据就可以正常预测没问题
x_data=np.linspace(-1,1,16, dtype=np.float32)[np.newaxis,:]
noise=np.random.normal(0,0.5,x_data.shape).astype(np.float32)
y_data=2*x_data+noise

#2.但是换成下面的热量数据测试就有问题
# path="orgData.xls"
# df=pd.read_excel(path)
#
# heatingPower=np.array(df.loc[:15,"瞬时热量(KW)"])
# inTemp=df.loc[:15,"进水温度 (℃)"]
# retTemp=df.loc[:15,"回水温度 (℃)"]
# innerTemp=df.loc[:15,"室内温度(℃)"]
# inputData=np.array((inTemp+retTemp)/2-innerTemp)
# heatingPower=np.matrix(heatingPower).getA()  #将(16,)维度转为为(1,16),当然还可以使用[　np.newaxis,:]
# inputData=inputData[np.newaxis,:]
#
# x_data=inputData              #(进水温度+回水温度)/2－室内温度　　作为数据的X
# y_data=heatingPower           #直接将供热功率作为数据的Y,即标签

# 3.原本以为是转换时候产生维度问题，但是把具体的数据写出来，还是有问题，难道真的是热量数据有问题
#  但是把热量点画出来，确实接近于正比例分布啊?
# x_data=np.array([29.25,28.25,28.2,28.25,27.8,23.35,23.5,24.3,24.25,24.4,
#    25.1,24.6,25.3,25.25,25.95,26.6]) [np.newaxis,:]
# y_data=np.array([3.871296,3.6894,3.56928,3.9182,3.432,3.0602,2.9172,
#    2.965248,2.827968,2.855424,3.075072,2.9172,3.075072,3.1746,
#    3.289,3.29472])[np.newaxis,:]  #这时原本的热量分析的数据，


print(x_data.shape,y_data.shape,)


#下面进行训练，下面没有区别，只是用上面三个不同的(x_data,y_data)对就会有问题
xs=tf.placeholder(tf.float32,[1,None])
ys=tf.placeholder(tf.float32,[1,None])

hiden_layer=add_layer(xs,1,10,active_function=tf.nn.relu)
pred=add_layer(hiden_layer,10,1,None)

loss=tf.reduce_mean(tf.square(ys-pred))

train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init=tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)


plt.figure()
#scatter中的数据点，可以是(n,)维度或者(n,1形式)
plt.scatter(x_data,y_data) #画出scatter图,这里可以使用(1,16)维的数据,也可以使用(16,1)维的图片

for step in range(100):
    #运行1000次梯度下降迭代
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    prediction_value = sess.run(pred, feed_dict={xs: x_data})

print(prediction_value) #预测值都是一样的，试了好几遍，是数据的原因？
#plot中的数据点，必须是(n,)维度或者(n,1形式)，所以这里对原本是(1,300)的x_data进行转置
plt.plot(x_data.T,prediction_value.T,"r-")
plt.show()