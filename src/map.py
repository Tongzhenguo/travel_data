# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import webbrowser
import pandas as pd
import urllib
import json

'''
    调用高德静态地图标记指定点，并在本地浏览器显示
'''
key = '945ae54516979776ab3ee717012c24d4' #请使用你申请的公钥
geocode_url = r'http://restapi.amap.com/v3/geocode/geo?address=%s&city=上海&output=JSON&key={key}'.format(key=key)
# 高德地图-->静态地图API地址
staticmap_url = r'http://restapi.amap.com/v3/staticmap?location=121.472644,31.231706&zoom=9&size=1024*768&key={key}&labels='.format(key=key)

def getHtml(url):
    '''
    读取查询地点对应的经纬度信息
    :param url: 查询地点的request
    :return: [lon,lat]
    '''
    page = urllib.urlopen(url)                #访问网页
    data = page.readline()                         #读入数据
    data_dic = json.loads(data)                    #转换成python->字典
    data_dic_geocodes = data_dic['geocodes'][0]   #获取geocodes信息，也是以字典存储
    data__dic_location = data_dic_geocodes['location']  # 获取location信息
    location = str(data__dic_location).split(",")   #处理locaiton成为List
    return location                                 #返回信息


def getStaticAmap( loc_list,lonlat_list, ):
    '''
    显示静态地图
    :param loc_list:要显示的标记名的list
    :param lonlat_list: 经纬度字符串的list
    :return:
    '''
    url_amap = staticmap_url
    for i in range( len(loc_list) ):
        if i == len(loc_list)-1:
            url_amap += r'{loc_labels},2,0,16,0xFFFFFF,0x008000:{lonlat}'.format( loc_labels=loc_list[i],lonlat=lonlat_list[i] )#增加labels
        else:
            url_amap += r'{loc_labels},2,0,16,0xFFFFFF,0x008000:{lonlat}|'.format(loc_labels=loc_list[i],
                                                                                lonlat=lonlat_list[i])  # 增加labels
    print url_amap
    webbrowser.open(url_amap)                                                     #打开本地浏览器

if __name__=='__main__':
    df = pd.read_csv('../data/science_spot.csv')
    del df['Unnamed: 0']
    df['高德对应经度'] = 0.0
    df['高德对应纬度'] = 0.0
    loc_list = []
    lonlat_list= []
    i=0
    while i<len(df):
          df_2=df.ix[i,0] #地址
          loc_list.append( df_2 )
          url_amap=geocode_url % df_2
          print url_amap
          loc=getHtml(url_amap)
          df.ix[i,4]=float(loc[0])
          df.ix[i,5]=float(loc[1])
          lonlat_list.append( ','.join(loc) )
          i+=1
    df.to_csv('../data/shanghai_science_lonlat.csv', index=False,encoding='utf-8')


    science_spot = pd.read_csv('../data/shanghai_science_lonlat.csv')
    science_spot['景点名称'] = science_spot['景点名称'].apply(lambda x: urllib.quote(str(x).replace('—', '').replace('·', '')[:15],)) #标签内容，字符最大数目为15
    science_spot['lonlat_str'] = science_spot['高德对应经度'].astype(str) +','+ science_spot['高德对应纬度'].astype(str)
    i = 0
    batch_size = 9 #API最大限制
    while i + batch_size < len(science_spot):
        loc_list = list(science_spot.ix[i:i+batch_size,:]['景点名称'].values)
        lonlat_list = list(science_spot.ix[i:i+batch_size,:]['lonlat_str'].values)
        getStaticAmap(loc_list, lonlat_list, )
        i += batch_size

