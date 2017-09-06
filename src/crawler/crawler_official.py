# coding=utf-8
import pandas as pd

def get_site():
    data = pd.read_csv('../../data/ctrip/ctrip_comments_.csv')
    def f(x):
        for i in str(x).split(' '):
            if 'http' in i:
                return i
        return ''
    df = pd.DataFrame()
    df['url']= data['poi_types'].apply(f)
    data = pd.read_csv('../../data/shanghai_science_lonlat.csv')
    df['name'] = data['景点名称']
    df[df['url']!=''].to_csv( '../../data/sci_website.csv',index=False )


