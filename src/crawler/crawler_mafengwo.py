# coding=utf-8
import csv
from time import sleep

import  pandas as pd
import requests
from bs4 import BeautifulSoup

sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
f = open(u'../../data/mafengwo/马蜂窝景点概览和点评.csv', 'wb')
f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
writer = csv.writer(f)
writer.writerow(['name','url','overview', 'commentlist'])
i = 0
for s in sci['景点名称'].values:
    i += 1
    url = 'http://www.mafengwo.cn/search/s.php?q=%s&t=poi' % (s)
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    content = soup.find(name='div',attrs={'class':'flt1'})
    a = content.find('a')
    if a:
        poi_url = a['href']
        res = requests.get(poi_url)
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        overview = soup.find(name='div',attrs={'data-anchor':'overview'})
        if  overview:
            overview = overview.text.replace(',',' ')
        else :
            overview= ''
        row = [s,poi_url,overview]
    else:
        row = [s,'','']
    writer.writerow(row)
    sleep(5)
    print '%s success!' % (s)