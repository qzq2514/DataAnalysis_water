import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from datetime import datetime

import matplotlib.dates as mdates

path='orgData.xls'
df=pd.read_excel(path)
# df=df.set_index(['采集时间'])
print(df.shape[0])

x=np.arange(df.shape[0])
plt.scatter(x,df['室外温度(℃)'])
timeSpan=[ind for ind in x if ind%1000==0]
plt.xticks(timeSpan,df['采集时间'][timeSpan],rotation=25,fontsize=6)
#print(df['室外温度(℃)'])



#或者也可以直接:plt.scatter(df['采集时间'],df['室外温度(℃)']),以字符串的时间作为x轴

plt.show()
