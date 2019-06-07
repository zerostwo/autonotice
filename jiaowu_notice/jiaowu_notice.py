import requests
import re
from lxml import etree
import yagmail
import datetime as d

def log_sicau(id, pwd, r):
    session = requests.Session()
    index = session.get('http://jiaowu.sicau.edu.cn/web/web/web/index.asp', timeout=2)
    index.encoding = 'gb2312'
    seletor=etree.HTML(index.text)
    sign = seletor.xpath("//input[@name='sign']/@value")
    data = {
        'user': id,
        'pwd': pwd,
        'lb': 'S',
        'submit': '',
        'sign': sign
    }
    try:
        post_url = 'http://jiaowu.sicau.edu.cn/jiaoshi/bangong/check.asp'
        session.post(post_url, data=data, timeout=2)
        data = session.get('http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/index1.asp', timeout=2)
        data.encoding = 'gb2312'
        log = open('./auto_notice.log', "a+")
        t = d.datetime.now().strftime("%Y-%m-%d %H:%M")
        yag = yagmail.SMTP(user="sicauer@126.com", password="981211Dd", host='smtp.126.com')
        # contents = ['<h3 align="center">News!</h3>']
        a = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>教务处最新动态</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>'
        b = '<body style="margin: 0; padding: 0;"><table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><h2 align="center">News!</h2></tr><tr>'
        c = ''
        dd = '</table><footer><p align = "center" style="text-align: center; font-size: 11px;">&copy;2019 <a href="https://sicauer.com" style="color: #000000;text-decoration:none;">Sicauer</a>, All Rights Reserved</p></footer></body></html>'
        # 获取教务网上的信息
        notice_set = re.compile('<font color=#339999>(.*)</font></a>').findall(data.text)
        # date_set = re.compile('class="bluetext">\((.*)\)<').findall(data.text)
        notice_url = re.compile('href="(.*)"><font color=#339999>').findall(data.text)
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
                notice = str(i+1) + '. ' "<a href = 'http://jiaowu.sicau.edu.cn/xuesheng/bangong/main/" + notice_url[i] + "' style='text-decoration:none;'>" + compare[i] + "</a>"
                # notice = date_set[i] + compare[i]
                # contents.append(notice)
                c += '<tr><p align="center">' + notice + '</p></tr>'
                print(t, "添加成功", compare[i], file=log)
            try:
                # html = '<p align = "center">Copyright 2018 <a href="https://zerostwo.github.io">Zerostwo</a></p>'
                # contents.append(html)
                con = a + b + '<h4 align="center">' + t + '</h4></tr>' + c + dd
                # print(con)
                for i in r:
                    yag.send(to=i, subject='教务处最新动态', contents=con)
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

r = []
user_file = open('../user.txt')
while True:
    line = user_file.readline()
    if line:
        r.append(line[:-1])
    else:
        break
user_file.close()
# print(r)
id = '201702420'
pwd = '981211'
log_sicau(id, pwd, r)

