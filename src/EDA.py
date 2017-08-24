# coding=utf-8
import json
import urllib

import pandas as pd


##题2 数据
'''
#########################景区拥堵分析#########################
'''
xls5 = pd.ExcelFile("/data/q2/数据集5_上海主要景点4-5月游客数量情况.xlsx")
xls5_sheet1 = xls5.parse(xls5.sheet_names[0])
print xls5_sheet1.head()
'''
    景点名称    人数                  时间 舒适度等级
0  朱家角古镇   570 2017-04-01 08:50:00  非常舒适
1  朱家角古镇   813 2017-04-01 09:20:00  非常舒适
2  朱家角古镇  1192 2017-04-01 09:50:00  非常舒适
3  朱家角古镇  1508 2017-04-01 10:20:00  非常舒适
4  朱家角古镇  1766 2017-04-01 10:50:00  非常舒适
'''
print xls5_sheet1.shape #(71850, 4)
crowd_event =  xls5_sheet1[xls5_sheet1[u'舒适度等级']==u'非常拥挤']
crowd_event['datetime'] = pd.to_datetime(crowd_event[u'时间'])
crowd_event['weekday'] = crowd_event['datetime'].apply(lambda x:1+x.weekday())#Monday == 0 ... Sunday == 6
crowd_event['hour'] = crowd_event['datetime'].apply(lambda x:x.hour)
crowd_event_cnt = crowd_event.groupby( [u'景点名称','weekday','hour'] )[u'舒适度等级'].count().reset_index()
crowd_event_cnt.columns = [u'景点名称','weekday','hour','count']
crowd_event_cnt = crowd_event_cnt.sort_values([u'景点名称','hour'])
def fn(x):
    a = list(set(x))
    a.sort()
    a = map(str, a)
    return '/'.join(a)
a = crowd_event_cnt.groupby(u'景点名称')['hour'].apply( lambda x:fn(x) ).reset_index()
b = crowd_event_cnt.groupby(u'景点名称')['weekday'].apply( lambda x:fn(x) ).reset_index()
crowd_ = pd.merge( a,b,on=u'景点名称' )
crowd_['crowd_dur'] = crowd_['hour'].apply(lambda s:len(str(s).split('/')) )
print crowd_
'''
          景点名称                              拥堵时段        拥护日期        拥堵时长
0     上海中医药博物馆                             10/14            3/4          2
1     上海共青森林公园                                14              6          1
2        上海动物园                 10/11/12/13/14/15            1/7          6
3    上海国际旅游度假区           11/12/13/14/15/16/17/18      1/4/5/6/7          8
4        上海植物园                          14/15/16          1/2/7          3
5      上海海洋水族馆                          13/14/15              7          3
6      上海炮台湾景区                                14              1          1
7      上海玻璃博物馆                       13/14/15/16      2/3/4/5/6          4
8      上海田子坊景区  10/11/12/13/14/15/16/17/18/19/20  1/2/3/4/5/6/7         11
9        上海科技馆                 10/11/12/13/14/15          1/6/7          6
10        上海豫园                       13/14/15/16          4/5/6          4
11    上海都市菜园景区            9/10/11/12/13/14/15/16        1/5/6/7          8
12    上海闵行体育公园                             10/15              1          2
13       上海闻道园                             11/13            1/7          2
14   上海马陆葡萄艺术村                          13/14/15              7          3
15     大宁郁金香公园                 11/12/13/14/15/16            1/7          6
16        新场古镇                          12/13/14            1/2          3
17       朱家角古镇                          12/13/14            1/7          3
18  金茂大厦88层观光厅                    16/17/18/20/21          1/6/7          5
19    长风海洋世界景区                       13/14/15/16          5/6/7          4
'''

user_loc = pd.read_csv("/data/q2/数据集1_用户地理位置.csv")
print user_loc.head()
'''
         日期  时段      用户标识         经度      纬度
0  20170401   0  21714645  121.48258  31.239
1  20170401   0  20734366  121.48258  31.239
2  20170401   0  20000169  121.48258  31.239
3  20170401   0  20368284  121.48258  31.239
4  20170401   0  21224649  121.48258  31.239
'''

'''
    转换成高德经纬度
'''
user_loc.to_csv('/data/q2/user_loc_log.csv')
points = user_loc[['经度','纬度']].drop_duplicates()
key = '945ae54516979776ab3ee717012c24d4' #请使用你申请的公钥
regeo_url = 'http://restapi.amap.com/v3/geocode/regeo?key={key}&location={lonlat}&extensions=all&batch=true'
points = pd.read_csv('../q2/points.csv')
address_list = []
def getHtml(url):
    '''
    读取查询地点对应的经纬度信息
    :param url: 查询地点的request
    :return: [lon,lat]
    '''
    page = urllib.urlopen(url)                #访问网页
    data = page.readline()                         #读入数据
    data_dic = json.loads(data)                    #转换成python->字典
    data_dic_regeocodes = data_dic['regeocodes'][0]   #获取geocodes信息，也是以字典存储
    data_dic_location = data_dic_regeocodes['formatted_address']  # 获取location信息
    location = data_dic_location  #处理locaiton成为List
    return location                                 #返回信息
for i in range( len(points) ):
    lonlat = str(points.ix[i,:]['经度']) +','+ str(points.ix[i,:]['纬度'])
    url = regeo_url.format(key=key, lonlat=lonlat)
    print url
    address_list.append( getHtml( url ) )
points['地址'] = address_list
def fn( x ):
    for i in ['上海迪士尼乐园','外滩','豫园城隍庙','人民广场','新天地']:
        if i in x:
            return i
    return '其他'
points['景点'] = points['地址'].apply( fn )
points.to_csv('/data/cache/point.csv',index=False,encoding='utf-8')

