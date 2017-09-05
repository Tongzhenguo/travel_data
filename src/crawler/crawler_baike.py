# coding=utf-8
from time import sleep

import  pandas as pd
import requests
from bs4 import BeautifulSoup

sci = pd.read_csv('../../data/shanghai_science_lonlat.csv')
i = 0
for s in sci['景点名称'].values:
    i += 1
    url = 'https://baike.baidu.com/item/%s' % (s)
    res = requests.get(url)
    res = res.text.encode(res.encoding).decode('utf-8')
    soup = BeautifulSoup(res, 'html.parser')
    content = soup.find(name='div',attrs={'class':'main-content'})
    if content:
        text = content.text
    else:
        text = ''
    with open('../../data/baike/%s.txt' % (str(i)),'w') as f:
        f.write(text)
    sleep(5)
    print '%s success!' % (s)