#coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import traceback
import time
from dateop import dateDelta,dateSub
import threading
from queue import Queue
from store import saveUrls
from mylog import logUrlConnectError,readErrorUrl,deleteErrorUrl
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1',
            'Pragma':'no-cache',
            'Cache-Control':'no-cache',

        }
'''

'''
class LookUp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        

    def run(self):
        global queue_date, mutex_date_get, mutex_date_put
        mutex_date_get.acquire()

        while queue_date.qsize() > 0:
            # 在线程池中取得链接和序号
            crawldate=str(queue_date.get())
            mutex_date_get.release()

            # 调用get_page函数
            result = get_page(crawldate)
            print('1111111111111111111111111111111111111122222222222222')
            print(result)
            print('111'*10)
            try:
                mutex_date_put.acquire()
                print(str(type(result)))
                if str(type(result))=="<class 'list'>":
                    #存储
                    print(len(result))
                    saveUrls(result)
                elif result==1:
                    logUrlConnectError(crawldate)
                mutex_date_put.release()
            except:
                traceback.print_exc()
                print('shittttttttttttttttttt')
                mutex_date_put.release()
                mutex_date_get.acquire()
                continue
            mutex_date_get.acquire()
        mutex_date_get.release()


def get_all(from_date, to_date):

    # 定义日期队列/得到日期的锁/给予日期的锁为全局变量
    global queue_date, mutex_date_get, mutex_date_put
    queue_date = Queue()
    threads = []
    # 线程数量
    num = 8
    mutex_date_get = threading.Lock()
    mutex_date_put = threading.Lock()
    #日期递减放入队列
    crawldate=to_date
    for k in range(dateDelta(from_date,to_date)+1):
        queue_date.put(str(crawldate))
        crawldate=dateSub(crawldate)

    for i in range(0, num):
        threads.append(LookUp())

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def get_page(crawldate):

    viewhref = "http://news.sina.com.cn/head/news{}am.shtml".format(crawldate)
    print(viewhref)
    time.sleep(1.5)
    try:
        r = requests.get(viewhref, timeout=30, headers=headers)
        r.encoding = r.apparent_encoding
        html=r.text
    except:
        #连接错误 logUrlConnectError
        return 1


    # 匹配某版块的新闻URL，应出现日期，且以“数字”.shtml结尾（不能以index.shtml结尾）
    # 早期网站URL以http开头，.html结尾，且日期年月日间没有“-”
    # financepat = re.compile(r'https?://finance.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # sportspat = re.compile(r'https?://sports.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # techpat=re.compile(r'https?://tech.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # entpat = re.compile(
    #     r'https?://ent.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # autopat = re.compile(
    #     r'https?://auto.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # edupat = re.compile(
    #     r'https?://edu.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # gamespat = re.compile(
    #     r'https?://games.sina.com.cn/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    # financelist = financepat.findall(html)
    # sportslist = sportspat.findall(html)
    # techlist=techpat.findall(html)
    # entlist=entpat.findall(html)
    # autolist=autopat.findall(html)
    # edulist=edupat.findall(html)
    # gameslist=gamespat.findall(html)
    newspat = re.compile(r'(https?://(?:\w+)\.sina\.com\.cn)/[^\[\]\<\>\"\'\s]*?/\d{4}-?\d\d-?\d\d/[^\[\]\<\>\"\'\s]*?\d+.s?html')
    newslist = newspat.findall(html)
    print(len(newspat))
    print(newspat)
    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    result=[]
    # result.extend([[i, '财经','0', nowtime] for i in financelist])
    # result.extend([[i, '科技', '0', nowtime] for i in techlist])
    # result.extend([[i, '体育','0', nowtime] for i in sportslist])
    # result.extend([[i, '娱乐', '0', nowtime] for i in entlist])
    # result.extend([[i, '汽车', '0', nowtime] for i in autolist])
    # result.extend([[i, '教育', '0', nowtime] for i in edulist])
    # result.extend([[i, '游戏', '0', nowtime] for i in gameslist])
    result.extend([[i, '新闻', '0', nowtime] for i in newslist])

    with open('urlList.txt','a+',encoding = 'utf-8') as fw:
        for i in result:
            fw.write( str(i)+ '\n')
        fw.close()
    return result

#重新爬取新闻URL
def getErrorUrlAgain():
    datelist=readErrorUrl()
    for crawldate in datelist:
        result=get_page(crawldate)
        try:
            if str(type(result)) == "<class 'list'>":
                # 存储
                saveUrls(result)
                deleteErrorUrl(crawldate)
            elif result == 1:
                logUrlConnectError(crawldate)
        except:
            traceback.print_exc()

