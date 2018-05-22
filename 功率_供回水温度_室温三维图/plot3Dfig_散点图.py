import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

df=pd.read_excel("orgData.xls")
gongTemp=df["Flow temperature (°C)"]
retTemp=df["Return temperature (°C)"]
kw=df["Power (kW)"]
sittingStemp=df["Temperature_sittingroomS(°C)"]

fig=plt.figure()
ax=Axes3D(fig)
sc=ax.scatter((gongTemp+retTemp)/2,kw,sittingStemp,c=sittingStemp,cmap=plt.cm.hot)
plt.colorbar(sc)
ax.set_xlabel('供回水平均值(℃)') #坐标轴
ax.set_ylabel('功率(℃)')
ax.set_zlabel('客厅南温度(℃)')
plt.show()

fig=plt.figure()
ax=Axes3D(fig)
#室温作为颜色指标,起到四维图的效果
sc=ax.scatter(kw,gongTemp,retTemp,c=sittingStemp,cmap=plt.cm.hot)
ax.set_xlim(2.5,4.8)
ax.set_xlabel('功率(℃)') #坐标轴
ax.set_ylabel('供水温度(℃)')
ax.set_zlabel('回水温度(℃)')
plt.colorbar(sc)
plt.show()
