import pandas as pd

pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
# 'jinjiang', 'qingyang',  'jinniu', 'tianfuxinqu', 'gaoxin7'
districts = ['wuhou', 'chenghua']
for district in districts:

    df = pd.read_csv("data/{}_beike.csv".format(district))

    df = df.join(df['house_info'].str.split("|", expand=True))
    df.rename(columns = {0:"楼层", 1:"建造时间", 2:"几室几厅", 3:"房屋面积", 4:"朝向"}, inplace=True)

    df = df.join(df['follow_info'].str.split("/", expand=True))
    df.rename(columns = {0:"关注人数", 1:"发布时间"}, inplace=True)

    df = df.replace("\n", "", regex=True).replace(" ", "", regex=True).replace("人关注", "", regex=True)\
        .drop(["house_info", "follow_info", "Unnamed: 0"], axis=1)\
        .rename(columns = {"name":"房屋名称", "href":"房屋链接", "position":"房屋位置", "position_href":"房屋位置链接",
                           "total_price":"房屋总价", "unit_price":"房屋单价"})


    df.to_csv("data/{}_beike_dwd_1.csv".format(district))
