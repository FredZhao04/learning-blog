import pandas as pd

pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)

districts = ['jinjiang', 'qingyang', 'wuhou', 'chenghua', 'jinniu', 'tianfuxinqu', 'gaoxin7']
for district in districts:
    df = pd.read_csv("data/{}_beike_dwd_1.csv".format(district))

    # 判断"房屋面积","朝向"是否为空

    df.loc[df["房屋面积"].isnull(), "房屋面积"] = df["建造时间"]
    df.loc[df["朝向"].isnull(), "朝向"] = df["几室几厅"]
    df.loc[~df["建造时间"].str.contains("年"), "建造时间"] = ""
    df.loc[~df["几室几厅"].str.contains("室|厅"), "几室几厅"] = ""

    df.loc[~df["几室几厅"].str.contains("室|厅") & df["楼层"].str.contains("室|厅"), "几室几厅"] = df["楼层"].str[-4:]
    df = df.drop(['Unnamed: 0'], axis=1)

    df.to_csv("data/{}_beike_dwd_2.csv".format(district))