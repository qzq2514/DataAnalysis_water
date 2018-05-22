import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import re
import copy
import openpyxl

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

#
# df=pd.read_excel("TempData.xlsx")
df=pd.read_csv("FullData.csv")
def handel(s):
    try:
        orgS=s
        isPM=s.find("下午")!=-1
        isZheng=s.find(".00.00.")!=-1
        s=re.sub(r"-1([67])",lambda m:"-201"+m.group(1),s)
        s=re.sub(r"月 ?","",s)      #05-11月-16 04.00.00.000000 下午
        ind = s.rindex(".00.000")
        s=s[:ind]
        ind1 = s.rindex(" ")
        ind2 = s.rindex(".")

        if isPM:
            s=s[:ind1+1]+str(int(s[ind1+1:ind2])+12)+s[ind2:]
        if s[ind1+1:ind1+3]=="24":
            s = s.replace("24.", "12.")
        #print("1--------------------", s)
        if isZheng:
            intstr="%02d"%(int(s[ind1 + 1:ind2]) -1)
            s = s[:ind1 + 1] + intstr + s[ind2:]
            s = s[:ind2 + 1] + "59" #+ s[ind2 + 5:]

        if isPM==False and s[ind1+1:ind1+3]=="12":
         s = s.replace("12.", "00.")
        timede=datetime.timedelta(hours=8)   #北京时间比格林尼治时间早八个小时
        s=datetime.datetime.strptime(s,"%d-%m-%Y %H.%M")+timede
        return s
    except:
        print("orgS:",orgS)
        return np.NaN

df["HY_TIME_STAMP"]=[handel(m) for m in df["HY_TIME_STAMP"]]

endData=datetime.datetime.strptime("2017-11-1 23:59:00","%Y-%m-%d %H:%M:%S")
timeLimit=df["HY_TIME_STAMP"]<endData        #截取日期，保证一年的时间跨度
ind=df[timeLimit].index
df=df.loc[ind,:]

df["TimeStamp"]=[m.timestamp() for m in df["HY_TIME_STAMP"]]
df=df.sort_values(by = ['HY_METER_NUMBER','HY_TIME_STAMP'],axis = 0,ascending = True)
df=df.reset_index(drop=True)

df['Hour']=[m.hour for m in df["HY_TIME_STAMP"]]
df['Day']=[m.day for m in df["HY_TIME_STAMP"]]
df['Month']=[m.month for m in df["HY_TIME_STAMP"]]
df['Weekday']=[m.weekday() for m in df["HY_TIME_STAMP"]]

df_copy=copy.deepcopy(df.groupby('HY_METER_NUMBER'))

def func(da):
    cha=da[1]-da[0]
    if(cha<0 or cha>300):        #消除异常数据
        return 0
    else:
        return da[1]-da[0]
def func2(da):
    cha=da[1]-da[0]
    if cha/60<=90:   #一小时内的用水量，最多半小时误差
        return 1
    else:
        return 0

print("len(df_copy):",len(df_copy))
mind=df["HY_TIME_STAMP"].min()
maxd=df["HY_TIME_STAMP"].max()
print("minData():",mind)
print("maxData():",maxd)
# cha=df["HY_TIME_STAMP"].max()-df["HY_TIME_STAMP"].min()
# print("差:",cha.total_seconds())
# print(maxd.timestamp()-mind.timestamp())

for user in df_copy:
    tempDf=user[1]        #得到分组的数据,添加"单位时间用水"和"check"列
    ind=tempDf.index
    df.loc[ind,"单位时间用水"]=tempDf['HY_ORG_VALUE'].rolling(2).apply(func)
    df.loc[ind, "check"] = tempDf['TimeStamp'].rolling(2).apply(func2)

df_copy=copy.deepcopy(df.groupby('HY_METER_NUMBER'))

vals={}             #计算夜间3:00-4:00用水量最高的20家
for user in df_copy:
    tempDf = user[1]  # 得到分组的数据
    number=tempDf.iloc[0,0]
    b1=tempDf["Hour"]==3
    b2 = tempDf["Hour"] == 4
    b3 = tempDf["check"] == 1
    ind = tempDf[(b1 | b2) & b3].index
    val=df.loc[ind,"单位时间用水"].sum()/1000
    vals[number]=val

a1=sorted(vals.items(), key=lambda d: d[1])
print("夜间3:00-4:00用水量:",a1)

vals={}             #计算每户全年用水量
for user in df_copy:
    tempDf = user[1]
    number=tempDf.iloc[0,0]
    b3 = tempDf["check"] == 1
    ind = tempDf[b3].index
    val=df.loc[ind,"单位时间用水"].sum()/1000
    vals[number]=val
a1=sorted(vals.items(), key=lambda d: d[1])
print("每户全年用水量:",a1)

# bb1=df['Hour']==0                #检查零点有用水的数据
# bb2=df['check']==1
# bb3=df['单位时间用水']>100
# ind=df[bb1 & bb2 & bb3].index
# print(df.loc[[10495,10496,10519,10520,10639,10640,10855,10856],:])

def getHour():
    hours = []
    for h in range(24):
        b1=df["Hour"]==h
        b2=df["check"]==1
        ind=df[b1 & b2].index
        v=df.loc[ind,"单位时间用水"].sum()/1000
        hours.append(v)
    return hours

def getMonth():
    months = []
    for m in range(1,13):
        b1=df["Month"]==m
        b2 = df["check"] == 1
        ind=df[b1 & b2].index
        v=df.loc[ind,"单位时间用水"].sum()/1000
        months.append(v)
    return months

def getWeekday():
    weekdays = []
    for w in range(7):
        b1=df["Weekday"]==w
        b2 = df["check"] == 1
        ind=df[b1 & b2].index
        v=df.loc[ind,"单位时间用水"].sum()/1000           #升变立方米
        weekdays.append(v)
    return weekdays

def getHourInMonth():
    for m in range(1, 13):
        arr=[]
        b1 = df["Month"] == m
        for h in range(24):
            b2 = df["check"] == 1
            b3 = df["Hour"] == h
            ind=df[b1 & b2 & b3].index
            v=df.loc[ind,"单位时间用水"].sum()/1000           #升变立方米
            arr.append(v)
        print("%d月:"%m)
        print(arr)

def getDaysInMonN(N):
    end=0
    if N==2:
        end=29
    elif N==7:
        end=32
    arr=[]
    b1 = df["Month"] == N
    for d in range(1,end):
        b2 = df["check"] == 1
        b3 = df["Day"] == d
        ind=df[b1 & b2 & b3].index
        v=df.loc[ind,"单位时间用水"].sum()/1000           #升变立方米
        arr.append(v)
    return arr

def getHourInWeek():
    for w in range(7):
        arr=[]
        b1 = df["Weekday"] == w
        b2 = df["check"] == 1
        for h in range(24):
            b3 = df["Hour"] == h
            ind=df[b1 & b2 & b3].index
            v=df.loc[ind,"单位时间用水"].sum()/1000           #升变立方米
            arr.append(v)
        print("星期%d:"%(w+1))
        print(arr)

print("len(df):",len(df))

# getHourInWeek()

# getHourInMonth()
#
# arrry=getDaysInMonN(7)
# print(arrry)
#
# arrry=getDaysInMonN(2)
# print(arrry)


# hourVal=getHour()
# print("小时:",hourVal)
# plt.figure()
# plt.bar(range(1,25),hourVal,facecolor="#9999ff",edgecolor="white")
# plt.xlim(0.5,24.5)
# plt.xlabel("小时")
# plt.ylabel("用水量(立方米)")
# plt.show()

# weekdayVal=getWeekday()
# print("星期:",weekdayVal)
# arrWeekday=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
# arrWeekday=[1,2,3,4,5,6,7]
# plt.bar(range(7),weekdayVal,facecolor="#9999ff",edgecolor="white")
# plt.xlabel("星期")
# plt.ylabel("用水量(立方米)")
# plt.xticks([1,2,3,4,5,6,7],arrWeekday)
# plt.show()

# monthVal=getMonth()
# print("月:",monthVal)
# plt.bar(range(1,13),monthVal,facecolor="#9999ff",edgecolor="white")
# arrMonth=["一","二","三","四","五","六","七月","八月","九月","十月","十一月","十二月"]
# plt.xlabel("月份")
# plt.ylabel("用水量(立方米)")
# plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12],arrMonth)
# plt.show()
#
# df.to_excel("Tempqzq.xls",index=False)
# print("OK")