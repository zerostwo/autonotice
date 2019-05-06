import requests
from bs4 import BeautifulSoup
import yagmail
import datetime as d


def notification(url, r):
    session = requests.Session()
    data = session.get(url,verify=False)
    data.encoding = data.apparent_encoding
    soup = BeautifulSoup(data.text, features="lxml")
    try:
        log = open('./auto_notice.log', "a+")
        t = d.datetime.now().strftime("%Y-%m-%d %H:%M")
        yag = yagmail.SMTP(user="zerostwo@126.com", password="981211Dd", host='smtp.126.com')
        a = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>食品学院本科教学管理通知</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>'
        b = '<body style="margin: 0; padding: 0;"><table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><h2 align="center">News!</h2></tr><tr>'
        c = ''
        dd = '</table><footer><h5 align = "center"><b>&copy;2019 <a href="https://sicauer.com" style="color: #000000;">Sicauer</a></b></h5></footer></body></html>'
        # 获取教务网上的信息
        notice_set = []
        notice_url = []
        for i in soup.find_all("a"):
            if i.get("title") is not None and i.get("href")[:8] == "../info/":
                spxy_url = "https://spxy.sicau.edu.cn"
                notice_set.append(i.get("title"))
                notice_url.append(spxy_url + i.get("href")[2:])
        # 获取本地上的信息
        info_set = []
        info_file = open('./info.txt')
        while True:
            line = info_file.readline()
            if line:
                info_set.append(line[:-1])
            else:
                break
        info_file.close()
        # 比较教务网上和本科信息的差别
        compare = [i for i in notice_set if i not in info_set]
        # 判断
        if len(compare) == 0:
            print(t, "无最新消息", file=log)
            print(t, "无最新消息")
        else:
            info_file = open('./info.txt', "a+")
            for i in range(0, len(compare)):
                print(compare[i], file=info_file)
                notice = str(i+1) + '. ' "<a href = '" + notice_url[i] + "' style='text-decoration:none;'>" + compare[i] + "</a>"
                # notice = date_set[i] + compare[i]
                # contents.append(notice)
                c += '<tr><p align="center">' + notice + '</p></tr>'
                print(t, "添加成功", compare[i], file=log)
            try:
                # html = '<p align = "center">Copyright 2019 <a href="https://zerostwo.github.io">Zerostwo</a></p>'
                # contents.append(html)
                con = a + b + '<h4 align="center">' + t + '</h4></tr>' + c + dd
#                 print(con)
                for i in r:
                    yag.send(to=i, subject='食品学院本科教学管理通知', contents=con)
                print(t, "发送成功", file=log)
                print(t, "发送成功")
            except:
                print(t, "发送失败", file=log)
                print(t, "发送失败")
            info_file.close()

    except:
        print(t, '出错', file=log)
        print(t, '出错')
    log.close()

# 本科教学管理
url = "https://spxy.sicau.edu.cn/bkjxgl/rcgl.htm"
r = []
user_file = open('./user.txt')
while True:
    line = user_file.readline()
    if line:
        r.append(line[:-1])
    else:
        break
user_file.close()
notification(url, r)
