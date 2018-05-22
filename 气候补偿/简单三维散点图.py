from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

fig=plt.figure()
ax=Axes3D(fig)

path="orgData.xls"
df=pd.read_excel(path)


buInd=df['室外温度(℃)']>=6550
df.loc[buInd,'室外温度(℃)']=df.loc[buInd,'室外温度(℃)']-6553.6

#print(df[df['二次供温(℃)']<45].index)
# df.to_excel("myOut.xls", sheet_name='数据')

ax.scatter(df['室外温度(℃)'],df['室内温度(℃)'],df['二次供温(℃)'],c='r')

ax.set_zlabel('二次供温(℃)') #坐标轴
ax.set_ylabel('室内温度(℃)')
ax.set_xlabel('室外温度(℃)')
plt.show()