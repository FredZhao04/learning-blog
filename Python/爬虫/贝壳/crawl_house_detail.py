import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

url = "https://cd.ke.com/ershoufang/19122517710100200150.html"
headers = {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
      }
r_obj = requests.get(url, headers)
#打印请求网页状态
print(r_obj.status_code)
print('======'  + '爬取网页:' + url)
bs = BeautifulSoup(r_obj.content, "lxml")
title = bs.find('h1', class_ = 'main').get('title')
print(title)
# all_data = pd.DataFrame()
#
# districts = ['jinjiang', 'qingyang', 'wuhou', 'chenghua', 'jinniu', 'tianfuxinqu', 'gaoxin7']
#
# #在此爬取楼盘前100页数据
# for district in districts:
#   print("Start the %s data craw." % district)
#   for i in range(1,50):
#       headers = {
#       "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
#       }
#       url = ("https://cd.ke.com/ershoufang/{}/pg{}co32/").format(district, i)
#       r_obj = requests.get(url, headers)
#       #打印请求网页状态
#       print(r_obj.status_code)
#       print('======'  + '爬取第{}个网页'.format(i))
#       bs = BeautifulSoup(r_obj.content, "lxml")
#
#       data = pd.DataFrame()
#
#       name_list = []
#       href_list = []
#       position_list = []
#       positon_href_list = []
#       house_info_list = []
#       follow_info_list = []
#
#       #寻找二手房描述信息
#       sell_list_content = bs.find_all('li', class_ = 'clear')
#       for content in sell_list_content:
#           # 房子名称
#           name = content.find('div', class_ = 'title').find('a')['title']
#           href = content.find('div', class_ = 'title').find('a')['href']
#           # 房子所在位置信息
#           position = content.find('div', class_ = 'positionInfo').find('a').text
#           positon_href = content.find('div', class_ = 'positionInfo').find('a').get('href')
#
#           # 房子信息
#           house_info = content.find('div', class_ = 'houseInfo').text
#
#           # 关注人数和发布日期
#           follow_info = content.find('div', class_ = 'followInfo').text
#
#           name_list.append(name)
#           href_list.append(href)
#           position_list.append(position)
#           positon_href_list.append(positon_href)
#           house_info_list.append(house_info)
#           follow_info_list.append(follow_info)
#
#       data['name'] = name_list
#       data['href'] = href_list
#       data['position'] = position_list
#       data['position_href'] = positon_href_list
#       data['house_info'] = house_info_list
#       data['follow_info'] = follow_info_list
#
#       all_data = all_data.append(data)
#
#       # 休息20s
#       time.sleep(random.randint(15, 25))
#
#   # 保存文件
#   all_data.to_csv("{}_beike.csv".format(district))
