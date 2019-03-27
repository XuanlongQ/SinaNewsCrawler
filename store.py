#coding=utf-8
import pymysql
import traceback
#数据库信息
host="10.245.144.96"
user="user"
passwd="123456"
charset="utf8"
database="sinanews2"
urlTable="newsurl"
contentTable="newscontent"

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
