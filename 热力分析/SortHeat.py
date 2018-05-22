import numpy as np
import pandas as pd
import xlwt
import copy

def handle(ReZhiBiao,Gongshui,HuiShui):   #理论流量计算公式中的一些参数
    path='orgData.xls'
    df=pd.read_excel(path)

    df['理论流量 (m³/h)']='N/A'  #初始化
    df["流量 比"]=''
    df["备注"]=''


    notZero=df['房屋面积(㎡)']!=0                 #找到房屋面积为空或为0的行，其备注为'无面积数据',流量比为'N/A'
    areaNotNull=df['房屋面积(㎡)'].notnull()

    ind1=df[~(notZero & areaNotNull)].index
    df.loc[ind1,'备注']='无面积数据'
    df.loc[ind1,'流量 比']=np.NaN

    stopHeat=df['客户状态'].str.match('停热')    #用户状态为“停热”且瞬时流量为0,则“流量比”列填充为N/A，“备注”列填充为“停热”
    momentZero=df['瞬时流量 (m³/h)']==0
    ind2=df[stopHeat & momentZero].index
    df.loc[ind2,'备注']='停热'
    df.loc[ind2,'流量 比']=np.NaN

    shunNaN=df[df['瞬时流量 (m³/h)'].isnull()].index  #没有瞬时流量，则备注为"无瞬时流量",流量比比为NaN
    df.loc[shunNaN,"流量 比"]=np.NaN
    df.loc[shunNaN,'备注']="无瞬时流量"


    giveHeat=df['客户状态'].str.match('供热')    #用户状态为“供热”且瞬时流量为0,则“备注”列填充为“流量异常”
    ind3=df[giveHeat & momentZero].index
    df.loc[ind3,'备注']='流量异常'

    giveHeat=df['客户状态'].str.match('停热')    #用户状态为“停热”且瞬时流量不为0,则“备注”列填充为“存在偷热嫌疑”
    geraterZeor=df['瞬时流量 (m³/h)']>0
    ind4=df[giveHeat & geraterZeor].index
    df.loc[ind4,'备注']='存在偷热嫌疑'



    # ReZhiBiao=1
    # Gongshui=3.5
    # HuiShui=3
    ind5=df[(notZero & areaNotNull) & ~(stopHeat & momentZero)].index
    df.loc[ind5,'理论流量 (m³/h)']=df.loc[ind5,'房屋面积(㎡)'].map(lambda x:(860*1e-6)*ReZhiBiao*x/(Gongshui-HuiShui))

    df.loc[ind5,"流量 比"]=df.loc[ind5,'瞬时流量 (m³/h)']/df.loc[ind5,'理论流量 (m³/h)']


    df['单元']=df['客户地址'].str.split('-').map(lambda x:x[1]+'-'+x[2])

    df=df.sort_values(by=['单元',"流量 比"],axis = 0,ascending = [True,True])
    df=df.reset_index()    #重置索引



    ind=0
    df_copy=copy.deepcopy(df.groupby('单元'))   #每个单元计算总流量比

    dff=pd.DataFrame()
    for area in df_copy:

        temp=area[1]
        notNaNind=temp[temp['流量 比'].notnull()].index

        #print(notNaNind)
        dff.loc[ind,'单元地址']="香榭里·黎明"+temp.loc[temp.index[0],'单元']
        dff.loc[ind, '总面积(㎡)']=temp['房屋面积(㎡)'].sum()

        dff.loc[ind, '抄表时间'] = temp.loc[temp.index[0],'抄表时间']
        shunSum=temp.loc[notNaNind,'瞬时流量 (m³/h)'].sum()
        lunSum=temp.loc[notNaNind, '理论流量 (m³/h)'].sum()

        dff.loc[ind, '总瞬时流量(m³/h)'] = shunSum
        dff.loc[ind, '总理论流量(m³/h)'] = lunSum
        dff.loc[ind, '总流量比'] = shunSum/lunSum

        #原在同一个sheet中添加'单元总流量比'
        #avg=temp.loc[notNaNind,'瞬时流量 (m³/h)'].sum()/temp.loc[notNaNind,'理论流量 (m³/h)'].sum()
        #df.ix[ind,'单元总流量比']=avg
        ind+=1


    biNaN=df[df['流量 比'].isnull()].index
    df.loc[biNaN,"流量 比"]='N/A'

    df=df.drop(['单元','index'],axis=1)

    writer = pd.ExcelWriter('out.xls')
    df.to_excel(writer,'全部用户',index=False)


    dff.to_excel(writer, '单元流量', index=False)
    writer.save()
