#coding=utf-8
import datetime
import time
#input eg:20181015 (type=str)
#output eg:20181016 (type=str)

#日期减1
def dateSub(datestr):
    nowdate=datetime.datetime.strptime(datestr,'%Y%m%d')
    lastdate=(nowdate+datetime.timedelta(days=-1)).strftime("%Y%m%d")
    #print(lastdate)
    return lastdate
#日期加1
def dateAdd(datestr):
    nowdate=datetime.datetime.strptime(datestr,'%Y%m%d')
    nextdate=(nowdate+datetime.timedelta(days=1)).strftime("%Y%m%d")
    #print(nextdate)
    return nextdate

#返回date2与date1相差几天
def dateDelta(date1,date2):
    d2=datetime.datetime.strptime(date2,'%Y%m%d')
    d1=datetime.datetime.strptime(date1,'%Y%m%d')
    delta=d2-d1
    return delta.days
