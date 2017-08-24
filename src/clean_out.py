# coding=utf-8
import itertools
import pandas as pd
'''
    爬虫数据清洗的代码
'''
def clean_data( ):
    out = pd.read_csv('../data/out.tsv', sep='\t', names=['url', 'title', 'start_date', 'args', 'out_path'])
    out['pois'] = out['out_path'].apply(lambda x: x.replace("'", "")[1:-1].replace(", ", "/"))
    out = out[out['pois'] != '']
    out['days'] = out['args'].apply(lambda x: x.replace("'", "")[1:-1].split(',')[0])
    out['start_date'] = out['args'].apply(lambda x: x.replace("'", "")[1:-1].split(',')[1].replace('-', ''))
    out['money'] = out['args'].apply(lambda x: x.replace('，', '').replace("'", "")[1:-1].split(',')[2])
    out['who'] = out['args'].apply(lambda x: x.replace('，', '').replace("'", "")[1:-1].split(',')[3][1:])
    out['title'] = out['title'].apply(lambda x:x.replace(',', ' '))
    out[['url', 'title', 'start_date', 'days', 'money', 'who', 'pois']].to_csv('../data/out.csv', index=False)

out = pd.read_csv( '../data/out.csv' )

loc_list = []
for s in out['pois'].values:
    ss = set(str(s).split('/'))
    loc_list.extend(list(itertools.combinations(ss, 2)))
df = pd.DataFrame()
df['point_pair'] = loc_list
df['cnt'] = 1
point_pair_cnt = df.groupby('point_pair')['cnt'].count().reset_index()
point_pair_cnt = point_pair_cnt.sort_values('cnt',ascending=False)
point_pair_cnt.to_csv( '../data/point_pair_cnt.csv' )
print point_pair_cnt.head(50)