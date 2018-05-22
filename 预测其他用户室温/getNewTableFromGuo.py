import numpy as np
import pandas as pd
import datetime

df=pd.read_excel("orgData/4-3-501郭/42966106热表.xls")
df_sittingroomS=pd.read_excel("orgData/4-3-501郭/16130044客厅南.xls")

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
    s=s.replace("/18 ","/2018 ")
    s = s.replace("/17 ", "/2017 ")
    s=s[:-3]
    return s

# print(handle("2/18/18 12:08 AM"))

#将带有PM,AM的12制时间转成24小时制的时间
df["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df["Timestamp"])]
df_sittingroomS["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M")
                               for m in map(handle,df_sittingroomS["Timestamp"])]



delta=30       #每30分钟分个组
begTime=datetime.datetime.strptime("2/2/2018 00:00","%m/%d/%Y %H:%M")
endTime=begTime+datetime.timedelta(minutes=delta)
tagTime=datetime.datetime.strptime("3/1/2018 0:0","%m/%d/%Y %H:%M")
newdf=pd.DataFrame(columns=["Timestamp", "Flow temperature (°C)",
                            "Return temperature (°C)", "Power (kW)",
                            "Temperature_sittingroomS(°C)"])

i=0
while begTime<tagTime:
    # print(begTime)
    info = pd.Series([str(begTime + datetime.timedelta(minutes=delta / 2))], index=["Timestamp"])

    #计算热量表平均值
    b1 = df["Timestamp"] > begTime
    b2 = df["Timestamp"] < endTime
    ind=df[b1 & b2].index
    #添加供水温度和回水温度平均值
    info=info.append(df.loc[ind,["Flow temperature (°C)","Return temperature (°C)"]].mean())
    timedel=df.loc[ind,"Timestamp"].max()-df.loc[ind,"Timestamp"].min()
    hourdel=timedel.total_seconds()/3600     #计算这半小时内的时间差(小时做单位)
    kwhdel=df.loc[ind,"Energy (kWh)"].max()-df.loc[ind,"Energy (kWh)"].min()
    if hourdel==0 or timedel==0:   #保证分母为0并且这半小时内不止一个时间点
        begTime += datetime.timedelta(minutes=delta)
        endTime += datetime.timedelta(minutes=delta)
        i += 1
        continue
    info=info.append(pd.Series([kwhdel/hourdel],index=["Power (kW)"]))
    #至此成功添加时间，供水温度，回水温度和平均值下的功率

    # 计算客厅南温度平均值
    b1 = df_sittingroomS["Timestamp"] > begTime
    b2 = df_sittingroomS["Timestamp"] < endTime
    ind = df_sittingroomS[b1 & b2].index
    temp = pd.Series(df_sittingroomS.loc[ind, ["Temperature (°C)"]].mean().values,
                                     index=["Temperature_sittingroomS(°C)"])
    info = info.append(temp)


    #info是每半个小时的相关温度信息,newdf添加一行
    newdf.loc[i] = info

    #更新时间和索引
    begTime += datetime.timedelta(minutes=delta)
    endTime += datetime.timedelta(minutes=delta)
    i += 1

#对于没有数值的时间段，直接丢失
newdf=newdf.dropna(axis=0,how="any")
newdf.to_excel("data/standardData.xls",index=False)