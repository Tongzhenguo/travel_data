# coding=utf-8
import json

import pandas as pd
import numpy as np
df1 = pd.read_csv('../../data/shanghai_science_lonlat.csv')[['景点名称','级别','高德对应经度','高德对应纬度']]
df1['id'] = df1.index
df1.columns = ['name','stars','lat','lon','id']
df1['stars'] = df1['stars'].apply(lambda x:len(str(x)))
# print(df1.head())

#######ctrip stats
def f(x):
    s = str(x).replace('/5分', '')
    if s == 'nan':return 2
    else:
        return int(2 * float(s))

df2 = pd.read_csv('../../data/ctrip/ctrip_comments_.csv')[['好评分','景色分','趣味分','性价比','poi_types']]
df2['good_comment_ratio'] = df2['好评分'].apply( f )
df2['interesting'] = df2['景色分'].astype(float)+df2['趣味分'].astype(float)
df2['interesting'] = df2['interesting'].apply( lambda x:int(x) if str(x)!='nan' else 2)
df2['cost_performance'] = df2['性价比'].apply( lambda x:2*int(x) if str(x)!='nan' else 2)

def get_science_topic( x ):
    s = str(x).replace('/',' ')
    t_list = s.split()
    science = 0
    for t in t_list:
        if 'http' in t:continue
        if t in '科技馆 植物园 动物园 观景台 现代建筑 博物馆 创意园区 水族馆 蜡像馆 影视城 展馆展览'.split():
            science+=1
    return 2 * science if science<5 else science

def get_health_topic( x ):
    s = str(x).replace('/',' ')
    t_list = s.split()
    health = 0
    for t in t_list:
        if 'http' in t:continue
        if t in '主题公园 城市公园 采摘 游乐场 摩天轮 森林 农场 花园 古迹 古塔 山 园林 农家乐 手工作坊'.split():
            health+=1
    return 2 * health if health<5 else health

def get_gaoduanyou_topic( x ):
    s = str(x).replace('/',' ')
    t_list = s.split()
    gaoduanyou = 0
    for t in t_list:
        if 'http' in t:continue
        if t in '海滨 沙滩 观景台 现代建筑 特色街区 创意园区'.split():
            gaoduanyou+=1
    return 2 * gaoduanyou if gaoduanyou < 5 else gaoduanyou

def get_sandbeach_topic( x ):
    s = str(x).replace('/',' ')
    t_list = s.split()
    sandbeach = 0
    for t in t_list:
        if 'http' in t:continue
        if t in '海滨 沙滩'.split():
            sandbeach+=1
    return 2 * sandbeach if sandbeach < 5 else sandbeach

def get_sport_topic( x ):
    s = str(x).replace('/',' ')
    t_list = s.split()
    sport = 0
    for t in t_list:
        if 'http' in t:continue
        if t in '主题公园 城市公园 特色街区 森林 农场 山 农家乐'.split():
            sport+=1
    return 2 * sport if sport < 5 else sport

def get_humanity_topic( x ):
    s = str(x).replace('/',' ')
    t_list = s.split()
    humanity = 0
    for t in t_list:
        if 'http' in t:continue
        if t not in '主题公园 城市公园 特色街区 森林 农场 山 农家乐 展馆展览 科技馆 观景台 现代建筑 森林 农场 蜡像馆 影视城 采摘 海滨 沙滩'.split():
            humanity+=1
    return 2 * humanity if humanity < 5 else humanity

df2['science'] = df2['poi_types'].apply( get_science_topic )
df2['health'] = df2['poi_types'].apply( get_health_topic )
df2['gaoduanyou'] = df2['poi_types'].apply( get_gaoduanyou_topic )
df2['sandbeach'] = df2['poi_types'].apply( get_sandbeach_topic )
df2['sport'] = df2['poi_types'].apply( get_sport_topic )
df2['humanity'] = df2['poi_types'].apply( get_humanity_topic )
df2 = df2.drop(axis=1,labels=['好评分','景色分','趣味分','性价比','poi_types'])
# print( df2.head() )

#######baidubaike info
# df3 = pd.DataFrame()
# price_list = []
# hour_list = []
# season_list = []
# start_time_list = []
# for i in range(1,82):
#     with open('../../data/baike/%d.txt' % i,'rb') as f:
#         price,hour,season,start_time = '免费','一天','四季皆宜','全天'
#         lines = f.readlines()
#         i = 0
#         for line in lines:
#             line = line.decode('utf8')
#             if '门票价格' in line:
#                 if price!='免费':continue
#                 for j in range(i+1,len(lines)):
#                     if lines[j].decode('utf8').startswith('\r\n'):continue
#                     else:
#                         price = lines[j][:-2].decode('utf8')
#                         break
#             if '游玩时长' in line:
#                 if hour != '一天': continue
#                 for j in range(i+1,len(lines)):
#                     if lines[j].decode('utf8').startswith('\r\n'):continue
#                     else:
#                         hour = lines[j][:-2].decode('utf8')
#                         break
#             if '适宜季节' in line or '适宜游玩季节' in line:
#                 if season != '四季皆宜': continue
#                 for j in range(i+1,len(lines)):
#                     if lines[j].decode('utf8').startswith('\r\n'):continue
#                     else:
#                         season = lines[j][:-2].decode('utf8')
#                         break
#             if '开放时间' in line:
#                 if start_time != '全天': continue
#                 for j in range(i+1,len(lines)):
#                     if lines[j].decode('utf8').startswith('\r\n'):continue
#                     else:
#                         start_time = lines[j][:-2].decode('utf8')
#                         break
#             i += 1
#         print(price,start_time,season,start_time)
#         price_list.append(price)
#         hour_list.append(hour)
#         season_list.append(season)
#         start_time_list.append(start_time)
# df3['price'] = price_list
# df3['hour'] = hour_list
# df3['season'] = season_list
# df3['start_time'] = start_time_list
# df3.to_csv('../../data/info.csv',encoding='utf8',index=False)
df3 = pd.read_csv('../../data/info.csv',encoding='utf8')

df4 = pd.read_csv('../../data/ctrip/ctrip_sight.csv',encoding='utf8',)[['summary']].fillna('暂未采集到 待稍后补充')
df4.columns = ['description_json']
df4['description_json'] = df4['description_json'].apply( lambda x:json.dumps( str(x).replace(',',' ').replace('，',' ')[:200] ) )  #

df6 = pd.read_csv('../../data/comfort_resort.csv',encoding='utf8')
df6.columns = ['comfort']
df = pd.concat( [df1,df4,df3,df2,df6],axis=1,join='inner' )

#####
# xls5 = pd.ExcelFile("../../data/数据集5_上海主要景点4-5月游客数量情况.xlsx")
# df5 = xls5.parse(xls5.sheet_names[0])
# def mapping( x ):
#     if x == '非常舒适':return 10
#     if x == '舒适':return 8
#     if x == '一般':return 6
#     if x == '拥挤':return 4
#     if x == '非常拥挤':return 2
# df5['舒适度等级'] = df5['舒适度等级'].apply(mapping)
# df5 = df5[['景点名称','舒适度等级']].groupby( ['景点名称'],as_index=False ).mean()
# df5['舒适度等级'] = df5['舒适度等级'].astype(int)
# df5.to_csv('../../data/comfort.csv',encoding='utf8',index=False)
#
# xls7 = pd.ExcelFile("../../data/数据集7_上海主要景点名单及POI经纬度信息.xlsx")
# df7 = xls7.parse(xls7.sheet_names[0])[['景点名称']]
# df6 = pd.merge( df7,df5,on='景点名称' )
# df6[['舒适度等级']].to_csv('../../data/comfort_resort.csv',encoding='utf8',index=False)

###tag
# for i in range(1,82):
#     with open('../../data/baike/%d.txt' % i,'rb') as f:
#         lines = f.readlines()
#         for line in lines:
#             line = line.decode('utf8')
#             if line.startswith('著名景点') or '旅游景点' in line or '详解' in line or '主要游玩项目' in line or '项目' in line:
#                 s

path = pd.read_csv('../../data/path_id.csv',names=['id','start_month','days','money','who','poi_seq'])
user = pd.read_csv('../../data/user.csv',names=['strategy_index',"sex","age",'province',"cost_level"])
data = pd.merge( path,user,left_on='id',right_on='strategy_index' )[[ 'poi_seq',"sex","age",'province',"cost_level" ]]
age_desc_json_list = []
sex_desc_json_list = []
area_desc_json_list = []
cost_desc_json_list = []
for s in list(df1['name'].values):
    if s == '上海国际旅游度假区':s='迪士尼'
    filter_df = data[data['poi_seq'].str.contains(s)]
    for f in ['age','sex','province','cost_level']:
        freq = filter_df[f].value_counts()
        int_dict = freq.to_dict()
        str_dict = {}
        for kw in int_dict:
            # if f == 'province': kw
            str_dict[str(kw)] = int(int_dict[kw])
        if f == 'age':
            if str_dict:
                age_desc_json_list.append(json.dumps( str_dict ))
            else:
                age_desc_json_list.append( json.dumps( {'6': 146, '5': 327, '4': 175, '1': 1, '3': 62, '7': 88, '8': 67, '2': 25} ) )
        if f == 'sex':
            if str_dict:
                sex_desc_json_list.append(json.dumps(str_dict))
            else:
                sex_desc_json_list.append( json.dumps({'0': 551, '1': 340}) )
        if f == 'province':
            if str_dict:
                area_desc_json_list.append(json.dumps(str_dict))
            else:
                area_desc_json_list.append( json.dumps({'甘肃省': 1, '河南省': 16, '江西省': 25, '北京市': 32, '天津市': 9, '陕西省': 3, '山东省': 26, '宁夏': 1, '江苏省': 365, '浙江省': 210, '山西省': 6, '黑龙江': 3, '广东省': 31, '上海市': 1, '辽宁省': 5, '吉林省': 2, '河北省': 9, '安徽省': 69, '重庆市': 4, '湖北省': 18, '福建省': 11, '湖南省': 13, '内蒙古': 1, '青海省': 1, '广西省': 5, '四川省': 11, '云南省': 5, '海南省': 5, '贵州省': 3}) )
        if f == 'cost_level':
            if str_dict:
                cost_desc_json_list.append(json.dumps(str_dict))
            else:
                cost_desc_json_list.append( json.dumps({'6': 48, '5': 44, '4': 103, '1': 226, '3': 161, '7': 99, '2': 210}) )

# tag_list = []
# for ln in open('../../data/tag.txt','rb').readlines():
#     tag_dict = {}
#     for i in ln.replace('、',' ').replace("“","").replace("”","")[1:]:
#         tag_dict[i] = 0.48
#     tag_list.append( json.dumps( tag_dict ) )

###tag
ctrip_rank = pd.read_csv('../../data/81jingdian_rank.csv')
ctrip_rank['ctrip_rank'] = 2*ctrip_rank['打分'].astype(int)
rank_dict = {}
rank_list = []
for s in df1['name'].values:
    i = 0
    for t in ctrip_rank[ '景点名' ].values:
        if s in t:
            rank_dict[s] = ctrip_rank.ix[i,2]
        i+=1
    rank_dict[s] = 2
    rank_list.append( rank_dict[s] )
drank = pd.DataFrame()
drank['ctrip_rank'] = rank_list
# print(drank.head())
# print(ctrip_rank[['ctrip_rank']].head())
tag_json_list = []
with open('../../data/tag.txt','rb') as f:
    while(True):
        line = f.readline().decode('utf8')
        if line:
            tag_dict = {}
            tags = line[1:].replace(",", " ").replace("、", " ").replace("“", "").replace("”", "").replace("《",
                                                                                                          "》").replace(
                "、", " ").split(" ")
            for tag in tags:
                if tag in  ['','\n']:continue
                tag_dict[tag] = 0.6
            tag_json_list.append(json.dumps(tag_dict))
        else:break
tag_df = pd.DataFrame()
tag_df['tag_json'] = tag_json_list
print(len(tag_df))
print( len(drank) )
df = pd.concat( [df1,df4,df3,df2,df6,tag_df,drank],axis=1,join='inner' )

df['age_desc_json'] = age_desc_json_list
df['sex_desc_json'] = sex_desc_json_list
df['area_desc_json'] = area_desc_json_list
df['cost_desc_json'] = cost_desc_json_list

df['figure_url'] = 'waiting'
df['video_url'] = 'waiting'
df['ctrip_rank'] = 1
df['local_rank'] = 1

df['eat_json'] = 'waiting'
df['look_json'] = 'waiting'
df['play_json'] = 'waiting'
df['shopping_json'] = 'waiting'
df['tag_json'] = 'waiting'


df = df[[ 'id','name','description_json','figure_url','video_url'
    ,'price','hour','season','start_time',''
    'interesting','stars','ctrip_rank','comfort','good_comment_ratio','cost_performance'
    ,'science','health','gaoduanyou','sandbeach','sport','humanity'
    ,'lat','lon','local_rank','eat_json','look_json','play_json','shopping_json',
    'tag_json','age_desc_json','sex_desc_json','area_desc_json','cost_desc_json']]

import json
import pandas as pd

sce = pd.read_csv('../../data/shanghai_science_lonlat.csv') #景点名称,级别,经度,纬度,高德对应经度,高德对应纬度

related_poi_list = []
for i in sce['景点名称'].values:
    d_list = {}
    for j in sce['景点名称'].values:
        if j==i:continue
        dis_lat = sce[ sce['景点名称']==i ]['高德对应经度'].values-sce[ sce['景点名称']==j ]['高德对应经度'].values
        dis_lon = sce[sce['景点名称'] == i]['高德对应纬度'].values - sce[sce['景点名称'] == j]['高德对应纬度'].values
        d = abs(dis_lat)+abs(dis_lon)
        d_list[j] = d
    d_list = sorted(d_list.items(),key=lambda k:k[1])
    related_poi_list.append( json.dumps( [ s[0] for s in d_list[:3] ] ) )
df['related_poi_json'] = related_poi_list

df.to_csv('../../data/scenic.csv',encoding='utf8',index=False,header=False,sep='\t')


'''
DROP TABLE IF EXISTS `mydb`.`scenic` ;

CREATE TABLE IF NOT EXISTS `mydb`.`scenic` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `description` VARCHAR(2000) NULL,
  `figure_url` VARCHAR(45) NULL,
  `video_url` VARCHAR(45) NULL,
  `price` VARCHAR(45) NULL,
  `hour` VARCHAR(45) NULL,
  `season` VARCHAR(45) NULL,
  `start_time` VARCHAR(180) NULL,
  `interesting` INT NULL,
  `stars` INT NULL,
  `ctrip_rank` INT NULL,
  `comfort` INT NULL,
  `good_comment_ratio` INT NULL,
  `cost_performance` INT NULL,
  `science` INT NULL,
  `health` INT NULL,
  `gaoduanyou` INT NULL,
  `sandbeach` INT NULL,
  `sport` INT NULL,
  `humanity` INT NULL,
  `lat` DOUBLE NULL,
  `lon` DOUBLE NULL,
  `local_rank` INT NULL,
  `eat_json` VARCHAR(45) NULL,
  `look_json` VARCHAR(45) NULL,
  `play_json` VARCHAR(45) NULL,
  `shopping_json` VARCHAR(45) NULL,
  `tag_json` VARCHAR(500) NULL,
  `age_desc_json` VARCHAR(180) NULL,
  `sex_desc_json` VARCHAR(80) NULL,
  `area_desc_json` VARCHAR(1000) NULL,
  `cost_desc_json` VARCHAR(180) NULL,
  `related_poi_json` VARCHAR(180) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


LOAD DATA INFILE "/var/lib/mysql-files/scenic.csv"
REPLACE INTO TABLE scenic
CHARACTER SET utf8
FIELDS TERMINATED BY "\t" ENCLOSED BY ""
;
'''