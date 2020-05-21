import redis
import pandas as pd

r = redis.Redis(host='62.234.6.149', port=4000, db=8)
# 'jinjiang', 'qingyang', 'wuhou', 'chenghua',
districts = [ 'jinniu', 'tianfuxinqu', 'gaoxin7']
for district in districts:
    print(district)
    df = pd.read_csv("data/{}_beike_dwd_2.csv".format(district))
    for href in df["房屋链接"]:
        # 设置链接的值为1，1：未爬取，0：已爬取
        print(href)
        r.set(href, "1")