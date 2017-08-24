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
def norm_clean():
    out = pd.read_csv('../data/out.csv')
    data = pd.read_csv('../data/data.csv')
    points = list(data['景点名称'].values)
    data.index = data['景点名称']
    cate_dict = data['poi三级分类'].to_dict()
    path_list = []
    cate_list = []
    for path in out['pois'].values:
        nodes = path.split('/')
        ps = []
        cs = []
        for n in nodes:
            if n in points:
                ps.append( n )
                cs.append( cate_dict[n] )
        path_list.append( '/'.join( ps ) )
        cate_list.append( '/'.join( cs ) )
    out['pois_'] = path_list
    out['pois_cate'] = cate_list
    out['uid'] = out.index
    out[['uid','pois_','pois_cate']].to_csv('../data/out_v2.csv',index=False)
def extract_seq(  ):
    out = pd.read_csv('../data/out_v2.csv')
    seq_list = []
    cate_seq_list = []
    uid_list = []
    for i in range( len(out) ):
        plist = out.iloc[i]['pois_'].split('/')
        clist = out.iloc[i]['pois_cate'].split('/')
        n = len(plist)
        for j in range(n):
            for k in range(3,n+1):
                if j+k>n:continue
                uid_list.append(out.iloc[i]['uid'])
                seq_list.append( '/'.join( plist[j:j+k] ) )
                cate_seq_list.append( '/'.join( clist[j:j+k] ) )
    df = pd.DataFrame( uid_list,columns=['uid'] )
    df['loc_seq'] = seq_list
    df['cate_seq'] = cate_seq_list
    df.to_csv('../data/seq.csv',index=False)

#
# out = pd.read_csv( '../data/out.csv' )
#
# loc_list = []
# for s in out['pois'].values:
#     ss = set(str(s).split('/'))
#     loc_list.extend(list(itertools.combinations(ss, 2)))
# df = pd.DataFrame()
# df['point_pair'] = loc_list
# df['cnt'] = 1
# point_pair_cnt = df.groupby('point_pair')['cnt'].count().reset_index()
# point_pair_cnt = point_pair_cnt.sort_values('cnt',ascending=False)
# point_pair_cnt.to_csv( '../data/point_pair_cnt.csv' )
# print point_pair_cnt.head(50)