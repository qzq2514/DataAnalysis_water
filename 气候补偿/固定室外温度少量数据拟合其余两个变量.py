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

#df.to_excel("out.xls",sheet_name="气候补偿数据")
df=df.sort_values(by=outTemp)

inner=20

rangIndGreater=df['室内温度(℃)']-inner==0#<0.5
rangIndLess=inner-df['室内温度(℃)']==0#<0.5
#print(df.loc[rangIndGreater & rangIndLess,'室内温度(℃)'])
z1 = np.polyfit(df.loc[rangIndGreater & rangIndLess,'室外温度(℃)'],
                df.loc[rangIndGreater & rangIndLess,'二次供温(℃)'],deg=4)
#[ -4.36912844e-03   1.02815187e-01  -9.25631352e-02  -8.72290878e-01
#5.46174561e+01]
#[ -4.36912844e-03   1.02815187e-01  -9.25631352e-02  -8.72290878e-01
# 5.46174561e+01]

# print(z1)
p1 = np.poly1d(z1)
yvals=p1(df.loc[rangIndGreater & rangIndLess,'室外温度(℃)'])


# plt.plot(df.loc[rangIndGreater & rangIndLess,'室外温度(℃)'],
#          df.loc[rangIndGreater & rangIndLess, '二次供温(℃)'],
#          '.',label='original values')     #将原始的散点画出来，用'*'代表一个点

plt.plot(df.loc[rangIndGreater & rangIndLess,'室外温度(℃)'],yvals, 'r',label='polyfit values')  #将拟合的曲线画出来
plt.text(0, 56, "室外温度%s(℃)时的曲线" % inner)

plt.ylim((50,58))
plt.xlabel('室外温度(℃)')                #增加轴名
plt.ylabel('供水温度(℃)')
plt.legend(loc=4)                      #loc=4右下角
plt.title('气候补偿拟合')
plt.show()
