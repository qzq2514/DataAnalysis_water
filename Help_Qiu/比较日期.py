import datetime
#比较大小
strftime = datetime.datetime.strptime("2017-11-02", "%Y-%m-%d")
strftime2 = datetime.datetime.strptime("2017-01-04", "%Y-%m-%d")
print("2017-11-02大于2017-01-04：",strftime>strftime2)



#得到日期范围内的所有时间
def getEveryDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list
# print(getEveryDay('2016-01-01','2017-05-11'))

#时间加减
t1=datetime.datetime.strptime("2/9/2018 12:58","%m/%d/%Y %H:%M")
t2=t1+datetime.timedelta(minutes=30)
print("t1:",t1," t2:",t2)