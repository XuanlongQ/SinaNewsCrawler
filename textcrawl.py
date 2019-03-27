# coding=utf-8
from bs4 import BeautifulSoup
import re
import requests
import traceback
import time
import threading
from queue import Queue
from store import saveInfo,readUrls,updateErrorFlag
from mylog import logContentConnectError


class LookUp(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global queue_viewhref, mutex_href_get, mutex_href_put
        mutex_href_get.acquire()

        while queue_viewhref.qsize() > 0:
            # 在线程池中取得链接和序号
            viewhref_and_id=queue_viewhref.get()
            id=viewhref_and_id[0]
            viewhref=viewhref_and_id[1]
            mutex_href_get.release()

            # 调用get_page函数
            result = get_page(viewhref)
            print('1111111111111111111111111111111111111122222222222222')
            print(result)
            print('111' * 10)
            try:
                mutex_href_put.acquire()
                print(str(type(result)))
                if str(type(result)) == "<class 'list'>":
                    # 存储
                    #print(len(result))
                    saveInfo(id,viewhref,result)
                elif result == 1: #连接错误
                    logContentConnectError(viewhref)
                    pass
                elif result == 2: #内容无法获取
                    updateErrorFlag(id)
                    pass
                mutex_href_put.release()
            except:
                traceback.print_exc()
                print('shittttttttttttttttttt')
                mutex_href_put.release()
                mutex_href_get.acquire()
                continue
            mutex_href_get.acquire()
        mutex_href_get.release()


def get_some():
    # 一次从数据库里获取1000条，获得的数量=1000返回1，>0且<1000返回0，=0返回-1,读取错误返回-2
    # 定义日期队列/得到日期的锁/给予日期的锁为全局变量
    global queue_viewhref, mutex_href_get, mutex_href_put
    queue_viewhref = Queue()
    threads = []
    # 线程数量
    num = 8
    mutex_href_get = threading.Lock()
    mutex_href_put = threading.Lock()

    hrefs=readUrls()
    if hrefs==1: #数据库读取错误
        return -2
    for item in hrefs:
        queue_viewhref.put(item) #id和url信息元组放入队列

    for i in range(0, num):
        threads.append(LookUp())

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    if len(hrefs)==1000:
        return 1
    elif len(hrefs)>0:
        return 0
    elif len(hrefs)==0:
        return -1

def get_all():

    while True:
        r=get_some()
        if r == -2:
            print("数据获取失败")
        elif r<=0:
            print("数据获取完毕")
            break

def get_page(viewhref):
    #viewhref = "http://finance.sina.com.cn/roll/2016-08-26/doc-ifxvitex8965842.shtml"
    print(viewhref)
    time.sleep(1.5)
    try:
        r = requests.get(viewhref, timeout=30) #不用加上headers
        r.encoding = r.apparent_encoding
        html = r.text
    except:
        # 连接错误 logUrlConnectError
        return 1
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('title')
    if title != None:
        title = title.getText().strip()
    else:
        title = ""

    # 提取keywords
    kwpat = re.compile('[Kk]eywords')
    keywords = soup.find('meta', attrs={'name': kwpat})
    if keywords != None:
        keywords = keywords.get('content')
    else:
        keywords = ""

    # 提取description
    depat = re.compile('[Dd]escription')
    descript = soup.find('meta', attrs={'name': depat})
    if descript != None:
        descript = descript.get('content')
    else:
        descript = ""

    #artipat1 = re.compile('article')  # 正文部分
    #article = soup.find('div', attrs={'class': artipat1})
    article = soup.find('div', attrs={'class':'article'})
    if article == None:
        artipat2 = re.compile('article|artibody')
        article = soup.find('div', attrs={'id': artipat2})
        if article == None:
            return 2 #未找到正文


    h1list = article.findAll('h1')
    stronglist = article.findAll('strong')
    plist = article.findAll('p')[:5]

    h1text = ""
    strongtext = ""
    ptext = ""

    #注意要去除不间断空白符和全角空白符
    for i in h1list:
        if type(i.getText())==str:
            h1text = h1text + i.getText().replace(u'\u3000', u' ').replace(u'\xa0', u' ') + "\n"
    for i in stronglist:
        if type(i.getText()) == str:
            strongtext = strongtext + i.getText().replace(u'\u3000', u' ').replace(u'\xa0', u' ') + "\n"
    for i in plist:
        if type(i.getText()) == str:
            ptext = ptext + i.getText().replace(u'\u3000', u' ').replace(u'\xa0', u' ') + "\n"

    nowtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    result = [title, keywords, descript, h1text, strongtext, ptext,nowtime]

    print(result)

    return result
if __name__=='__main__':
    get_all()