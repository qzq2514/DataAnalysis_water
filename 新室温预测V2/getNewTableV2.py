import numpy as np
import pandas as pd
import datetime

df=pd.read_excel("dataOrg22-226.xls")    #已经整理好的2.2~2.26的数据(不包括室外温度)
df_outTemp=pd.read_excel("黎明院小区历史分钟列表.xlsx")    #获得室外温度

df_outTemp["采集时间"]=[datetime.datetime.strptime(str(m),"%Y/%m/%d %H:%M:%S") for m in df_outTemp["采集时间"]]

delta=30       #每30分钟分个组
newdf=pd.DataFrame(columns=["Timestamp","Energy (kWh)","Volume (m³)",
                            "Power (kW)","Flow temperature (°C)","Return temperature (°C)",
                            "Temperature_bedroom(°C)","Temperature_studyroom(°C)",
                            "Temperature_sittingroomN(°C)","Temperature_sittingroomS(°C)",
                            "Temperature_outer(°C)"])

for i in range(len(df)):
    info = df.loc[i]         #获得原始数据表的信息
    midTime=datetime.datetime.strptime(df.loc[i,"Timestamp"],"%Y-%m-%d %H:%M:%S")
    begTime = midTime - datetime.timedelta(minutes=delta/2)
    endTime = midTime + datetime.timedelta(minutes=delta / 2)

    b1 = df_outTemp["采集时间"] > begTime
    b2 = df_outTemp["采集时间"] < endTime
    ind = df_outTemp[b1 & b2].index
    temp = pd.Series(df_outTemp.loc[ind, ["室外温度(℃)"]].mean().values, index=["Temperature_outer(°C)"])
    info = info.append(temp)
    newdf.loc[i] = info

# #对于没有数值的时间段，直接丢失
newdf=newdf.dropna(axis=0,how="any")
newdf.to_excel("data22-226.xls",index=False)