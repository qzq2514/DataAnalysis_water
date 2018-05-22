import numpy as np
import pandas as pd
import datetime

df=pd.read_excel("热表（42966106）.xls")
df_bedroom=pd.read_excel("次卧（16130251）.xls")
df_studyroom=pd.read_excel("书房（16130261）.xls")
df_sittingroomN=pd.read_excel("客厅北（16130266）.xls")
df_sittingroomS=pd.read_excel("客厅南（16130044）.xls")

def handle(s):
    s_list=list(s)
    ind1 = s.index(" ")
    ind2 = s.rindex(":")
    # print(ind2)
    if s.find("PM") != -1:
        s = s[:ind1+1]+str(int(s[ind1+1:ind2])+12)+s[ind2:]   #将PM时间变为24小时制
        # ind2 = s.rindex(":")
        # print(ind2)
        if s[ind1+1:ind1+3]=="24":
         s=s.replace("24:","12:")
    elif s[ind1+1:ind1+3]=="12":         #    2/5/18 12:08 AM 变成 2/5/2018 0:08
        s = s.replace("12:", "0:")
    s=s.replace("/18","/2018")
    s=s[:-3]
    return s

# print(handle("2/5/18 12:08 AM"))

#将带有PM,AM的12制时间转成24小时制的时间
df["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df["Timestamp"])]
df_bedroom["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df_bedroom["Timestamp"])]
df_studyroom["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df_studyroom["Timestamp"])]
df_sittingroomN["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df_sittingroomN["Timestamp"])]
df_sittingroomS["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df_sittingroomS["Timestamp"])]


df=df.sort_values(by='Timestamp')
# print(df[20:40])

delta=30       #每30分钟分个组
begTime=datetime.datetime.strptime("2/2/2018 0:00","%m/%d/%Y %H:%M")
endTime=begTime+datetime.timedelta(minutes=delta)
tagTime=datetime.datetime.strptime("2/9/2018 23:59","%m/%d/%Y %H:%M")
newdf=pd.DataFrame(columns=["Timestamp","Energy (kWh)","Volume (m³)",
                            "Power (kW)","Flow temperature (°C)","Return temperature (°C)",
                            "Temperature_bedroom(°C)","Temperature_studyroom(°C)",
                            "Temperature_sittingroomN(°C)","Temperature_sittingroomS(°C)"])

i=0
while begTime<tagTime:
    # print(begTime)
    info = pd.Series([str(begTime + datetime.timedelta(minutes=delta / 2))], index=["Timestamp"])

    #计算热量表平均值
    b1 = df["Timestamp"] > begTime
    b2 = df["Timestamp"] < endTime
    ind=df[b1 & b2].index
    info=info.append(df.loc[ind,["Energy (kWh)","Volume (m³)",
                            "Power (kW)","Flow temperature (°C)","Return temperature (°C)"]].mean())

    #计算次卧温度平均值
    b1 = df_bedroom["Timestamp"] > begTime
    b2 = df_bedroom["Timestamp"] < endTime
    ind = df_bedroom[b1 & b2].index
    temp=pd.Series(df_bedroom.loc[ind, ["Temperature (°C)"]].mean().values,index=["Temperature_bedroom(°C)"])
    info = info.append(temp)
    # print(info)

    #计算书房温度平均值
    b1 = df_studyroom["Timestamp"] > begTime
    b2 = df_studyroom["Timestamp"] < endTime
    ind = df_studyroom[b1 & b2].index
    temp = pd.Series(df_studyroom.loc[ind, ["Temperature (°C)"]].mean().values, index=["Temperature_studyroom(°C)"])
    info = info.append(temp)

    # 计算客厅北温度平均值
    b1 = df_sittingroomN["Timestamp"] > begTime
    b2 = df_sittingroomN["Timestamp"] < endTime
    ind = df_sittingroomN[b1 & b2].index
    temp = pd.Series(df_sittingroomN.loc[ind, ["Temperature (°C)"]].mean().values, index=["Temperature_sittingroomN(°C)"])
    info = info.append(temp)

    # 计算客厅南温度平均值
    b1 = df_sittingroomS["Timestamp"] > begTime
    b2 = df_sittingroomS["Timestamp"] < endTime
    ind = df_sittingroomS[b1 & b2].index
    temp = pd.Series(df_sittingroomS.loc[ind, ["Temperature (°C)"]].mean().values,index=["Temperature_sittingroomS(°C)"])
    info = info.append(temp)


    #info是每半个小时的相关温度信息,newdf添加一行
    newdf.loc[i] = info

    #更新时间和索引
    begTime+=datetime.timedelta(minutes=delta)
    endTime+=datetime.timedelta(minutes=delta)
    i+=1

#对于没有数值的时间段，直接丢失
newdf=newdf.dropna(axis=0,how="any")
newdf.to_excel("orgData.xls",index=False)