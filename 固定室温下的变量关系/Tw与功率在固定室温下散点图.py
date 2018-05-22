import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path="orgData.xls"
df=pd.read_excel(path)


buInd=df['室外温度(℃)']>=6550
df.loc[buInd,'室外温度(℃)']=df.loc[buInd,'室外温度(℃)']-6553.6

x_data=df['室外温度(℃)']
y_data=df['瞬时热量(KW)']

colorMap=df['室内温度(℃)']
plt.figure()
# plt.scatter(df['室外温度(℃)'],df['室内温度(℃)'])  #直接画出室内室外温度散点图
# plt.xlabel("室外温度(℃)")
# plt.ylabel("室外温度(℃)")

sc=plt.scatter(x_data,y_data,c=colorMap,cmap=plt.cm.hot)  #不同室温带有不同颜色的散点图
plt.colorbar(sc)
plt.xlabel("室外温度")
plt.ylim(1.8,4.5)
plt.ylabel("功率")
plt.show()