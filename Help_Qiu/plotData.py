from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#保证正常显示汉字
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

path='orgData.xls'
df=pd.read_excel(path)

dates=df['采集时间']                      #获得数据集列
secWenCha=df['二次温差(℃)']
secCalcu=df['二次供水温度计算值(℃)']

#输入的起止日期格式
format='%Y/%m/%d %H:%M:%S'
start_str="2017/12/1 0:08:40"
end_str="2017/12/21 20:48:50"

start=datetime.strptime(start_str,format)
end=datetime.strptime(end_str,format)

xs = pd.Series([datetime.strptime(d,format) for d in dates])

great=xs>=start
less=xs<=end

index_range=xs[great & less].index
x_data=[datetime.strptime(str(d), '%Y-%m-%d %H:%M:%S') for d in xs[great & less]]


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(format))
plt.plot(x_data, df.loc[index_range,'二次温差(℃)'],label="二次温差(℃)")
plt.plot(x_data, df.loc[index_range,'二次供水温度计算值(℃)'],label="二次供水温度计算值(℃)")
plt.legend()
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.show()


