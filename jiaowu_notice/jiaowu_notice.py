import requests
from bs4 import BeautifulSoup
import datetime as d
import yagmail


t = d.datetime.now().strftime("%Y-%m-%d %H:%M")

url = "http://jiaowu.sicau.edu.cn/web/web/web/gwmore.asp"
r = requests.get(url)
r.encoding = r.apparent_encoding
soup = BeautifulSoup(r.text, features="lxml")
title = soup.find_all("font", {"color": "#339999"})
classification = soup.find_all("td", {"class": "welcome_style"})
url = soup.find_all("a")

infoList = []
for i in range(int(len(classification)/6)):
    dic = {
        "time": classification[6*i+3].string,
        "campus": classification[6*i+5].string,
        "classification": classification[6*i+1].string,
        "title": title[i].string,
        "url": "http://jiaowu.sicau.edu.cn/web/web/web/" + url[66:][i].get("href")
    }
    infoList.append(dic)

# 读取已发送信息
with open("info.txt") as f:
    readlines = f.readlines()
infoLog = []
for i in readlines:
    infoLog.append(i.strip())

# 读取发送对象
with open("../users.txt") as f:
    users = f.readlines()

# 打开日志文件    
log = open('./auto_notice.log', "a+")

titles = []
urls = []
for i in infoList:
    if i["campus"] == "雅安" or i["campus"] == "全校":
        titles.append(i["title"])
        urls.append(i["url"])

# 比较已发送和爬取到的信息，筛选出未发送的
compare = [i for i in titles if i not in infoLog]

# 邮件模板
yag = yagmail.SMTP(user="sicauer@126.com", password="981211Dd", host='smtp.126.com')
header = '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>教务处最新动态</title><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>'
body = '<body style="margin: 0; padding: 0;"><table border="0" cellpadding="0" cellspacing="0" width="100%"><tr><h2 align="center">News!</h2></tr><tr>'
main = ''
footer = '</table><footer><p align = "center" style="text-align: center; font-size: 11px;">&copy;2019 <a href="https://sicauer.com" style="color: #000000;text-decoration:none;">Sicauer</a>, All Rights Reserved</p></footer></body></html>'

notice = []
if len(compare) == 0:
    print(t, "无最新消息", file = log)
else:
    info_file = open("info.txt", "a+")
    for i in range(len(compare)):
        print(compare[i], file = info_file)
        for j in infoList:
            if j["title"] == compare[i]:
                url = j["url"]
        notice = str(i+1) + '. ' "<a href = '" + url + "' style='text-decorati on:none;'>" + compare[i] + "</a>"
        main += '<tr><p align="center">' + notice + '</p></tr>'
        print(t, "添加成功", compare[i], file=log)
        print(t, "添加成功", compare[i])
    try:
        con = header + body + '<h4 align="center">' + t + '</h4></tr>' + main + footer
        for i in users:
            yag.send(to=i, subject='教务处最新动态', contents=con)
            print(t, "发送成功", file=log)
            print(t, "发送成功")
    except:
        print(t, "发送失败", file=log)
        print(t, "发送失败")
    info_file.close()
log.close()
