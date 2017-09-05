# coding=utf-8
import csv
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
# f = open(u'../../data/ctrip/ctrip_search_stats.csv', 'wb')
# f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
# writer = csv.writer(f)
# writer.writerow(['景点名称','全部','景点','住宿', '美食','购物','交通','玩乐','问答','游记','目的'])
#
# for s in sci['景点名称'].values:
#     url = 'http://you.ctrip.com/searchsite/%s?query=%s' % ('', s)
#     res = requests.get(url)
#     res = res.text.encode(res.encoding).decode('utf-8')
#     soup = BeautifulSoup(res, 'html.parser')
#     content = soup.find(name='ul', attrs={'class': 'list-tabs'})
#     name2pos = ['全部','景点','住宿', '美食','购物','交通','玩乐','问答','游记','目的']
#     if content:
#         stats = [s, '', '', '', '', '', '', '','','','']
#         for a in content.find_all('a'):
#             print a.text.strip()[:2]
#             stats[ 1+name2pos.index( a.text.strip()[:2] ) ] = a.find('span').text.strip()
#         writer.writerow( stats )
#     else:
#         writer.writerow(stats)
#     print stats
#     sleep(5)
#     print '%s success!' % (s)
#     f.flush()
# f.close()

f = open(u'../../data/ctrip/ctrip_sight.csv', 'wb')
f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
writer = csv.writer(f)
writer.writerow(['景点名称','sight_url','summary'])
for s in sci['景点名称'].values:
    type = 'Sight'#,'Sight','Travels'
    url = 'http://you.ctrip.com/searchsite/%s?query=%s' % (type,s)
    res = requests.get(url)
    row = [s,'','']
    if res:
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(name='div', attrs={'class': 'result'})
        if content:
            score = 0
            sight_url = ''
            for li in  content.find_all('li'):
                if int(li.find('dd').find('a').text[:-3])>score:
                    sight_url = li.find('a')['href']
            print 'http://you.ctrip.com' + sight_url
            res = requests.get('http://you.ctrip.com' + sight_url)
            res = res.text.encode(res.encoding).decode('utf-8')
            soup = BeautifulSoup(res, 'html.parser')
            summary = soup.find(name='div',attrs={'class':'des_wide f_right'})
            summary = summary.text.strip().replace(',',' ')
            # row = [s,summary_url,summary]
    writer.writerow(row)
    f.flush()
    sleep(5)
    print '%s success!' % (s)
f.close()