import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

#'jinjiang', 'qingyang','wuhou', 'chenghua', 'jinniu', 'tianfuxinqu',
districts = ['qingyang']

#在此爬取楼盘前100页数据
for district in districts:
  print("Start the %s data craw." % district)
  all_data = pd.DataFrame()
  for i in range(1, 100):
      headers = {
      "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
      }
      url = ("https://wh.ke.com/ershoufang/{}/pg{}co32/").format(district, i)
      r_obj = requests.get(url, headers)
      #打印请求网页状态
      print(r_obj.status_code)
      print('======'  + '爬取第{}个网页'.format(i))
      bs = BeautifulSoup(r_obj.content, "lxml")

      data = pd.DataFrame()

      name_list = []
      href_list = []
      position_list = []
      positon_href_list = []
      house_info_list = []
      follow_info_list = []
      total_price_list = []
      unit_price_list = []

      #寻找二手房描述信息
      sell_list_content = bs.find_all('li', class_ = 'clear')
      for content in sell_list_content:
          # 房子名称
          name = content.find('div', class_ = 'title').find('a')['title']
          href = content.find('div', class_ = 'title').find('a')['href']
          # 房子所在位置信息
          position = content.find('div', class_ = 'positionInfo').find('a').text
          positon_href = content.find('div', class_ = 'positionInfo').find('a').get('href')

          # 房子信息
          house_info = content.find('div', class_ = 'houseInfo').text

          # 关注人数和发布日期
          follow_info = content.find('div', class_ = 'followInfo').text

          #房屋总价和单价
          total_price = content.find("div", class_="totalPrice").find("span").text
          unit_price = content.find("div", class_="unitPrice").find("span").text

          name_list.append(name)
          href_list.append(href)
          position_list.append(position)
          positon_href_list.append(positon_href)
          house_info_list.append(house_info)
          follow_info_list.append(follow_info)
          total_price_list.append(total_price)
          unit_price_list.append(unit_price)

      data['name'] = name_list
      data['href'] = href_list
      data['position'] = position_list
      data['position_href'] = positon_href_list
      data['house_info'] = house_info_list
      data['follow_info'] = follow_info_list
      data['total_price'] = total_price_list
      data['unit_price'] = unit_price_list

      all_data = all_data.append(data)

      # 休息20s
      time.sleep(random.randint(15, 25))

  # 保存文件
  all_data.to_csv("data/{}_beike.csv".format(district))
