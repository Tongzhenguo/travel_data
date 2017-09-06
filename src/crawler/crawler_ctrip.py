# coding=utf-8
import csv
from time import sleep

import pandas as pd
import requests
from bs4 import BeautifulSoup

def crawler_comments():
    sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
    f = open(u'../../data/ctrip/ctrip_comments_.csv', 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
    writer = csv.writer(f)
    writer.writerow(['景点名称','sight_url','好评分','景色分','趣味分','性价比','comment_content','address','poi_types'])
    for s in sci['景点名称'].values:
        type = 'Sight'#,'Sight','Travels'
        url = 'http://you.ctrip.com/searchsite/%s?query=%s' % (type,s)
        print url
        res = requests.get(url)
        row = [s]
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
                if sight_url != '':
                    print 'http://you.ctrip.com' + sight_url
                    row.append( 'http://you.ctrip.com' + sight_url )
                    res = requests.get('http://you.ctrip.com' + sight_url)
                    res = res.text.encode(res.encoding).decode('utf-8')
                    soup = BeautifulSoup(res, 'html.parser')
                    comment_summary = soup.find(name='dl',attrs={'class':'comment_show'})
                    if comment_summary:
                        for score in comment_summary.find_all(name='span',attrs={'class':'score'}):
                            row.append( score.text )
                    sightcommentbox = soup.find(name='div', attrs={'id': 'sightcommentbox'})
                    if sightcommentbox:
                        comment_content = []
                        for comment_single in sightcommentbox.find_all(name='span',attrs={'class':'heightbox'}):
                            comment_content.append( comment_single.text.replace(',','') )
                    comment_content = '     '.join( comment_content )
                    row.append( comment_content )
                    row.append( soup.find( name='p',attrs={'class':'s_sight_addr'} ).text.split('：')[1].strip() )
                    s_sight_in_list = soup.find(name='ul',attrs={'class':'s_sight_in_list'})
                    poi_types = []
                    for a in s_sight_in_list.find_all('a'):
                        poi_types.append( a.text )
                    row.append( ' '.join( poi_types ) )
                else:
                    row = [s, '', '', '', '', '', '','', '']
            else:
                row = [s,'','','','','','','', '']
        else:
            row = [s, '', '', '', '', '', '','', '']
        print row
        writer.writerow(row)
        f.flush()
        sleep(5)
        print '%s success!' % (s)
    f.close()
crawler_comments()

def crawler_stats(  ):
    sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
    f = open(u'../../data/ctrip/ctrip_search_stats.csv', 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
    writer = csv.writer(f)
    writer.writerow(['景点名称','全部','景点','住宿', '美食','购物','交通','玩乐','问答','游记','目的'])

    for s in sci['景点名称'].values:
        url = 'http://you.ctrip.com/searchsite/%s?query=%s' % ('', s)
        res = requests.get(url)
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(name='ul', attrs={'class': 'list-tabs'})
        name2pos = ['全部','景点','住宿', '美食','购物','交通','玩乐','问答','游记','目的']
        if content:
            stats = [s, '', '', '', '', '', '', '','','','']
            for a in content.find_all('a'):
                print a.text.strip()[:2]
                stats[ 1+name2pos.index( a.text.strip()[:2] ) ] = a.find('span').text.strip()
            writer.writerow( stats )
        else:
            writer.writerow(stats)
        print stats
        sleep(5)
        print '%s success!' % (s)
        f.flush()
    f.close()
def crawler_place( ):
    sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
    f = open(u'../../data/ctrip/ctrip_search_stats.csv', 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
    writer = csv.writer(f)
    writer.writerow(['景点名称','全部','景点','住宿', '美食','购物','交通','玩乐','问答','游记','目的'])

    for s in sci['景点名称'].values:
        url = 'http://you.ctrip.com/searchsite/%s?query=%s' % ('', s)
        res = requests.get(url)
        res = res.text.encode(res.encoding).decode('utf-8')
        soup = BeautifulSoup(res, 'html.parser')
        content = soup.find(name='ul', attrs={'class': 'list-tabs'})
        name2pos = ['全部','景点','住宿', '美食','购物','交通','玩乐','问答','游记','目的']
        if content:
            stats = [s, '', '', '', '', '', '', '','','','']
            for a in content.find_all('a'):
                print a.text.strip()[:2]
                stats[ 1+name2pos.index( a.text.strip()[:2] ) ] = a.find('span').text.strip()
            writer.writerow( stats )
        else:
            writer.writerow(stats)
        print stats
        sleep(5)
        print '%s success!' % (s)
        f.flush()
    f.close()
def crawler_sight():
    sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
    f = open(u'../../data/ctrip/ctrip_sight.csv', 'wb')
    f.write(unicode('\xEF\xBB\xBF', 'utf-8'))   # 文件头
    writer = csv.writer(f)
    writer.writerow(['景点名称','sight_url','summary'])
    for s in sci['景点名称'].values:
        type = 'Sight'#,'Sight','Travels'
        url = 'http://you.ctrip.com/searchsite/%s?query=%s' % (type,s)
        print url
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
                if sight_url != '':
                    print 'http://you.ctrip.com' + sight_url
                    res = requests.get('http://you.ctrip.com' + sight_url)
                    res = res.text.encode(res.encoding).decode('utf-8')
                    soup = BeautifulSoup(res, 'html.parser')
                    summary = soup.find(name='div',attrs={'class':'text_style'})
                    if summary:
                        print summary.text
                        summary = summary.text.strip().replace(',',' ')
                        row = [s,sight_url,summary]
        writer.writerow(row)
        f.flush()
        sleep(5)
        print '%s success!' % (s)
    f.close()