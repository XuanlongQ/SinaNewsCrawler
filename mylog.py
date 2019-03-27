#----------------------------日志记录---------------------
#爬取URL的界面如果加载错误，记录
def logUrlConnectError(crawldate):
    with open('error_url_connect.txt', 'a+') as f:
        datelist = f.read().splitlines()
        if crawldate not in datelist:
            f.write(str(crawldate))
            f.write('\n')
#读取爬URL错误的记录
def readErrorUrl():
    datelist=[]
    with open('error_url_connect.txt','r') as f:
        datelist=f.read().splitlines()

    return datelist
#重新爬取成功，删除log
def deleteErrorUrl(crawldate):
    with open('error_url_connect.txt', 'r+') as f:
        datelist = f.read().splitlines()
        #文件指针指向开头并删除所有记录
        f.seek(0)
        f.truncate()
        if crawldate not in datelist:
            f.write(str(crawldate))
            f.write('\n')

#爬取新闻界面如果连接错误，记录
def logContentConnectError(viewhref):
    with open('error_content_connect.txt', 'a+') as f:
        hreflist = f.read().splitlines()
        if viewhref not in hreflist:
            f.write(str(viewhref))
            f.write('\n')