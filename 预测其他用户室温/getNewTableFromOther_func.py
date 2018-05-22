import numpy as np
import pandas as pd
import datetime

def func(path1,path2,n):
    #4-1-2001/39055058热表.xls
    #4-1-2001/16130016客厅南.xls
    df=pd.read_excel("orgData/%s"%path1)
    df_sittingroomS=pd.read_excel("orgData/%s"%path2)

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


    #将带有PM,AM的12制时间转成24小时制的时间
    #2018-02-27 13:56:53
    df["抄表时间"]=[datetime.datetime.strptime(m,"%Y-%m-%d %H:%M:%S") for m in df["抄表时间"]]
    df_sittingroomS["Timestamp"]=[datetime.datetime.strptime(m,"%m/%d/%Y %H:%M") for m in map(handle,df_sittingroomS["Timestamp"])]


    # print(df_sittingroomS.loc[:10,"Timestamp"])
    delta=60*6       #每6个小时分个组(因为数据太少)
    begTime=datetime.datetime.strptime("12/28/2017 0:0","%m/%d/%Y %H:%M")
    endTime=begTime+datetime.timedelta(minutes=delta)
    tagTime=datetime.datetime.strptime("3/1/2018 23:59","%m/%d/%Y %H:%M")
    newdf=pd.DataFrame(columns=["Timestamp", "Flow temperature (°C)",
                                "Return temperature (°C)", "Power (kW)",
                                "Temperature_sittingroomS(°C)"])

    i=0
    while begTime<tagTime:
        # print(begTime)
        info = pd.Series([str(begTime + datetime.timedelta(minutes=delta / 2))], index=["Timestamp"])

        #计算热量表平均值
        b1 = df["抄表时间"] > begTime
        b2 = df["抄表时间"] < endTime
        ind=df[b1 & b2].index
        #添加供水温度和回水温度平均值
        info = info.append(pd.Series(df.loc[ind,["进水温度 (℃)"]].mean().values, index=["Flow temperature (°C)"]))
        info = info.append(pd.Series(df.loc[ind, ["回水温度 (℃)"]].mean().values, index=["Return temperature (°C)"]))
        # info=info.append(df.loc[ind,["进水温度 (℃)","回水温度 (℃)"]].mean())

        timedel=df.loc[ind,"抄表时间"].max()-df.loc[ind,"抄表时间"].min()
        hourdel=timedel.total_seconds()/3600     #计算这半小时内的时间差(小时做单位)
        kwhdel=df.loc[ind,"累积能量 (kWh)"].max()-df.loc[ind,"累积能量 (kWh)"].min()

        if hourdel==0 or timedel==0:   #保证分母为0并且这半小时内不止一个时间点
            begTime += datetime.timedelta(minutes=delta)
            endTime += datetime.timedelta(minutes=delta)
            i += 1
            continue
        # print(kwhdel/hourdel)
        info=info.append(pd.Series([kwhdel/hourdel],index=["Power (kW)"]))

        #至此成功添加时间，供水温度，回水温度和平均值下的功率

        # 计算客厅南温度平均值
        b1 = df_sittingroomS["Timestamp"] > begTime
        b2 = df_sittingroomS["Timestamp"] < endTime
        ind = df_sittingroomS[b1 & b2].index
        temp = pd.Series(df_sittingroomS.loc[ind, ["Temperature (°C)"]].mean().values,
                                         index=["Temperature_sittingroomS(°C)"])
        info = info.append(temp)

        # print(info)
        #info是每半个小时的相关温度信息,newdf添加一行
        newdf.loc[i] = info

        #更新时间和索引
        begTime += datetime.timedelta(minutes=delta)
        endTime += datetime.timedelta(minutes=delta)
        i += 1

    #对于没有数值的时间段，直接丢失
    newdf=newdf.dropna(axis=0,how="any")
    newdf.to_excel("data/data%s.xls"%n,index=False)