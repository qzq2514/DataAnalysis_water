from datetime import datetime
import pandas as pd
import numpy as np

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

path='data.xls'
df=pd.read_excel(path)

dates = df['采集时间']

#字符串日期转datetime型
xs = [datetime.strptime(d, '%Y/%m/%d %H:%M:%S') for d in dates]


# print()
#坐标轴的日期显示形式,这里显示到秒
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %H:%M:%S'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator())
# 画散点图
print(type(xs))
print(type(df['室外温度(℃)']))
plt.scatter(xs, df['室外温度(℃)'])
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.show()