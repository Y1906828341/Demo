import re
import requests
from bs4 import BeautifulSoup
import pymysql
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/70.0.3538.110 Safari/537.36'}
url = 'http://news.huse.edu.cn/zhxw/'
res = requests.get(url, headers=headers, params={'wd': 'python'})
res.encoding = 'utf-8'
html = res.text
soup_html = BeautifulSoup(html, features='html.parser')
# print(soup_html.prettify())
last_page = soup_html.find('td')
# print(last_page)
last_page = str(last_page)
num = re.findall(r' /+(.*?)页', last_page)
num = int(num[0])+1
print(num)
x = 1
for j in range(1, num):  # int(num[0]) + 1
    each_page_url = 'http://wzq.huse.cn/catalog/15284/pc/index_{}.shtml'.format(j)
    each_page_res = requests.get(each_page_url, headers=headers, params={'wd': 'python'})
    each_page_res.encoding = 'utf-8'
    if (each_page_res.status_code == 200):
        each_html = each_page_res.text
        each_soup_html = BeautifulSoup(each_html, features='html.parser')
        each_list_2 = each_soup_html.find(class_='list-2')
        each_li = each_list_2.find_all(class_='tit')
        each_Time = each_list_2.find_all(class_='time')
        for k in range(0, len(each_li)):
            for_each_title = each_li[k].get_text()
            for_each_Time = each_Time[k].get_text()
            print('【{0}】[{1}]'.format(x, k + 1), each_Time[k].get_text(), each_li[k].get_text())
            # 连接数据库
            conn = pymysql.connect(host='localhost', user='Guard', password='123456', database='mysite')
            cursor = conn.cursor()
            sql = "INSERT INTO huse_news(title,timer) VALUES (%s,%s);"
            title = for_each_title
            timer = for_each_Time
            cursor.execute(sql, [title, timer])
            conn.commit()
            cursor.close()
            conn.close()
            time.sleep(2)
            print('{}写入数据库成功！'.format(for_each_title))
    else:
        continue
    x += 1
    # print(list_2)
    # print(list_2)
