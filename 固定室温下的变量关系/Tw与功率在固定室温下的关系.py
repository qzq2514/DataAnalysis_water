import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

#def handle(inner):
path="orgData.xls"
df=pd.read_excel(path)

outTemp='室外温度(℃)'
inTemp='室内温度(℃　)'

buInd=df['室外温度(℃)']>=6550
df.loc[buInd,'室外温度(℃)']=df.loc[buInd,'室外温度(℃)']-6553.6
df=df.sort_values(by=outTemp)    #先矫正室外温度

for inner in np.arange(19,25):
    upper=df['室内温度(℃)']-inner<0.4
    less=inner-df['室内温度(℃)']<0.4

    x_data=df.loc[upper & less,'室外温度(℃)']
    y_data_fit=df.loc[upper & less,'瞬时热量(KW)']

    print(y_data_fit.shape)
    z1 = np.polyfit(x_data,y_data_fit,deg=1)
    fx = np.poly1d(z1)


    x_data=np.arange(-3,12)
    y_data = fx(x_data)
    plt.plot(x_data,y_data, 'b')  #将拟合的曲线画出来
    x_data=np.array(x_data)
    # x_data=x_data.reset_index()
    # print(type(y_data))
    # print(x_data[1])
    # # print(x_data[103])
    # print(y_data[1])
    plt.text(x_data[1], y_data[1], "%s(℃)" % inner)
plt.xlabel("室外温度")
plt.ylabel("功率")
plt.show()