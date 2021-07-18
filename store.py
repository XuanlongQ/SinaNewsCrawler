#coding=utf-8
import pymysql
import traceback
import json

#数据库信息
host="xxx"
user="xxx"
passwd="xxx"
charset="utf8"
database="xxx"
urlTable="xxx"
contentTable="xxx"

'''
#----------------Mysql操作---------------------------------
def saveUrls(hreflist):  # tagname在此默认与table名称相同
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, db=database, charset=charset)
        cur = conn.cursor()
        sql = "INSERT ignore INTO {} (url,tag1,flag,gaintime) VALUE(%s,%s,%s,%s)".format(urlTable)  # 用(%d,%s)会报错，pymysql的自身bug
        print(sql)

        for item in hreflist:
            cur.execute(sql, item)
        conn.commit()
        print("URL存储成功！")
    except Exception as e:
        print("存储URL时出错！")
        print(e)
        conn.rollback()
    finally:
        conn.close()
'''      
#----------------Saveurl操作---------------------------------
# list:
    # result.extend([[i, '财经','0', nowtime] for i in financelist])
    # result.extend([[i, '科技', '0', nowtime] for i in techlist])
    # result.extend([[i, '体育','0', nowtime] for i in sportslist])
    # result.extend([[i, '娱乐', '0', nowtime] for i in entlist])
    # result.extend([[i, '汽车', '0', nowtime] for i in autolist])
    # result.extend([[i, '教育', '0', nowtime] for i in edulist])
    # result.extend([[i, '游戏', '0', nowtime] for i in gameslist])
def saveUrls(hreflist):
    # jsonList = []
    # hrefItem = {}
    # hrefItem['url'] = hreflist[0]
    # hrefItem['type'] = hreflist[1]
    # hrefItem['category'] = hreflist[2]
    # hrefItem['time'] = hreflist[3]
    # jsonList.append(hrefItem)
    # hrefJson = json.dumps(hrefItem,ensure_ascii=False)
    for i in hreflist:
        print(i)
        print('(*****未抓取的url*******)')
        continue
        # with open('urlList.txt','a+',encoding = 'utf-8') as fw:
        #     fw.write(hrefJson + '\n')
        #     fw.close()

'''
def readUrls(count=1000):
    try:
        urllist = []
        conn = pymysql.connect(host=host, user=user, password=passwd, db=database, charset=charset)
        cur = conn.cursor()

        sql = "select id,url from {} where flag=0 limit ".format(urlTable) + str(count)
        # print(sql)
        cur.execute(sql)
        results = cur.fetchall()
        #print(results) #元组类型
        #for item in results:
        #   urllist.append(list(item))
        #print(urllist)
        conn.close()
        print(len(results))
        return results
    except:
        print("读取URL时数据库错误!")
        # traceback.print_exc()
        conn.close()
        return 1
'''
  
# hrefs=readUrls()，def readUrls(count=1000):
def readUrls():
    path = r'/Users/xuanlongqin/Documents/urlList.txt'
    hrefs = []
    with open(path,'r',encoding= 'utf-8') as fr:
        for newline in fr:
            data = newline.replace('[','').replace(']','').replace("'",'').split(',')
            # print(data[0])
            hrefs.append(data[0])
            # print(hrefs)
        fr.close()
            
    return tuple(hrefs)


'''
def saveInfo(id,viewhref,result):
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, db=database, charset=charset)
        cur = conn.cursor()
        #print(result)
        sql1="INSERT ignore INTO {} (id,url,title,keywords,description,h1,strong,ptext,gaintime) " \
             "VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(contentTable)
        result.insert(0,id)
        result.insert(1,viewhref)
        cur.execute(sql1,result)
        conn.commit()

        sql2="update {} set flag=1 where id=%s".format(urlTable)
        cur.execute(sql2,id)
        conn.commit()
        print("网页信息存储成功！")
    except Exception as e:
        print("存储网页信息时出错！")
        #print(e)
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()
'''


# result = [publishTime,title, keywords, descript, strongtext, nowtime]
def saveInfo(viewhref,result):
    try:
        cPath = 'DecemberJson.txt'
        aItem = {}
        # aList = []
        aItem['publishTime'] = result[0]
        aItem['url'] = viewhref
        aItem['title'] = result[1]
        aItem['keywords'] = result[2]
        aItem['descript'] = result[3]
        aItem['content'] = result[4]
        # aList.append(aItem)
        # print(aList)
        dataList = json.dumps(aItem,indent=4,ensure_ascii=False)
        with open(cPath,'a+',encoding='utf-8') as fw:
            fw.write(dataList + ',' + '\n')
            fw.close()
    except Exception as e:
        print("错误：",str(e))

    

def updateErrorFlag(id):
    try:
        conn = pymysql.connect(host=host, user=user, password=passwd, db=database, charset=charset)
        cur = conn.cursor()
        sql = "update {} set flag=2 where id=%s".format(urlTable)
        cur.execute(sql, id)
        conn.commit()

        print("flag更新成功！")
    except Exception as e:
        print("flag更新时出错！")
        print(e)
        conn.rollback()
    finally:
        conn.close()

if __name__=='__main__':
    readUrls()


'''
# 获取总条数
def readUrlNum(tagname):
    try:
        urllist = []
        conn = pymysql.connect(host=host, user=user, password=passwd, db=database, charset=charset)
        cur = conn.cursor()
        sql = "select count(1) from " + tagname
        cur.execute(sql)
        num = cur.fetchone()
        conn.close()
        return int(num[0])

    except:
        print("读取URL数量时数据库错误!")
        traceback.print_exc()
        conn.close()
        return []

'''
