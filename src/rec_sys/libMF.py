# coding=utf-8
import csv
import os

import gc

import numpy
import pandas as pd

#w(x) = log( 1+N('view') / N(x) ),实际评分和w(x)=1一样
import time

"""
    基于矩阵分解的推荐算法
    使用的台大开源的libMF包
    先根据SGD优化MSE,得到用户矩阵和物品矩阵（脚本：libMF.sh）
    然后计算每一个用户对每一个商品的评分，选择top20，去掉看过的，生成top5推荐列表
    麻烦的是全量计算的时间复杂度非常高，而且效果还差
    最终使用test中的top10筛选的候选物品
"""

def get_action_weight( x):
    pass

def make_train_test(  ):
    train = pd.read_csv('../data/train.csv')
    user = pd.read_csv('../data/candidate.txt')
    item = pd.read_csv('../data/all_news_info.csv')

    #将user_id和item_id重新映射成连续的id
    uid_uniqid = user[['user_id']].sort_values(['user_id'])
    uid_uniqid.index = user['user_id'].values
    uid_uniqid['user_id'] = range(len(uid_uniqid))
    uid_uniqid = uid_uniqid['user_id'].to_dict()

    iid_uniqid = item[['item_id']].sort_values(['item_id'])
    iid_uniqid.index = item['item_id'].values
    iid_uniqid['item_id'] = range(len(iid_uniqid))
    iid_uniqid = iid_uniqid['item_id'].to_dict()

    train['weight'] = train['action_type'].apply(get_action_weight)
    train = pd.merge(user, train, on='user_id')
    rat_mat = train[['user_id', 'item_id', 'weight']].groupby(['user_id', 'item_id'], as_index=False).sum()
    rat_mat['user_id'] = rat_mat['user_id'].apply( lambda x: uid_uniqid.get(x) )
    rat_mat['item_id'] = rat_mat['item_id'].apply( lambda x: iid_uniqid.get(x) )
    rat_mat['weight'] = rat_mat['weight'].apply(float)
    rat_mat.to_csv('../data/real_matrix.tr.txt', index=False, header=False,sep=" ")

def save_user_mat( factor_num, ):
    f = open('../model/libMF_model_l1l2', 'r')
    user_mat_csv = open('../data/user_mat.csv', 'w')
    csv_writer = csv.writer(user_mat_csv,delimiter=',')
    csv_writer.writerow( ['uniqid', 'flag']+["factor_" + str(i) for i in range(factor_num)] )
    n = 0
    while( True ):
        line = f.readline()
        if(line.startswith("p")):
            #去掉p标志
            ss = line[1:].strip().split(" ")
            csv_writer.writerow( ss )
            n += 1
        if( n % 1000 == 0 ): print("write lines "+str(n))
        if ( line == None or line.startswith("q") ):
            break
    f.close()
    user_mat_csv.close()
    print(' write all lines '+str(n) )

def save_item_mat( factor_num, ):
    f = open('../model/libMF_model_l1l2', 'r')
    item_mat_csv = open('../data/item_mat.csv', 'w')
    csv_writer = csv.writer(item_mat_csv,delimiter=',')
    csv_writer.writerow( ['uniqid', 'flag']+["factor_" + str(i) for i in range(factor_num)] )
    n = 0
    while( True ):
        line = f.readline()
        if(line.startswith("q")):
            #去掉标志
            ss = line[1:].strip().split(" ")
            csv_writer.writerow( ss )
            n += 1
        if( n % 1000 == 0 ): print("write lines "+str(n))
        if ( not line ):
            break
    f.close()
    item_mat_csv.close()
    print(' write all lines '+str(n) )

def help( p ):
    ss = str(p).split(",")
    rec,viewed = ss[0],ss[1]
    rec = list( rec.split(" ") )
    viewed_list = list( set( viewed.split(" ") ) )
    size = 0
    for i in rec:
        size += 1
        if i in viewed_list:
            rec.remove( i )
            size -= 1
        if size == 5:break

    rec = " ".join( rec[:5])
    return rec

def addAndSortTopK( e,sorted_list,k=60 ):
    if( len(sorted_list)<k ):
        sorted_list.append( e )
    if( len(sorted_list)>=k and e[1]>sorted_list[k-1][1] ):
        sorted_list.append( e )
        sorted_list.sort(key=lambda x:-x[1])
    return sorted_list


def make_predict( num_factor ):
    print(' 读取用户和物品矩阵 ')
    user_mat = pd.read_csv('../data/user_mat.csv')
    item_mat = pd.read_csv('../data/item_mat.csv')
    item = pd.read_csv('../data/news_info.csv')
    train = pd.read_csv('../data/train.csv')
    user = pd.read_csv('../data/candidate.txt')
    item_all = pd.read_csv('../data/all_news_info.csv')

    print(' 将uniqid重新映射成user_id,item_id ')
    uniqid_uid = user[['user_id']].sort_values(['user_id'])
    uniqid_uid.index = range(len(uniqid_uid))
    uniqid_uid = uniqid_uid['user_id'].to_dict()

    uniqid_iid = item_all[['item_id']].sort_values(['item_id'])
    uniqid_iid.index = range(len(uniqid_iid))
    uniqid_iid = uniqid_iid['item_id'].to_dict()

    user_mat['user_id'] = user_mat['uniqid'].apply( lambda x:uniqid_uid[x] )
    item_mat['item_id'] = item_mat['uniqid'].apply( lambda x: uniqid_iid[x] )

    print( ' 预测评分 ' )
    rec = pd.DataFrame()
    user_list = []
    rec_items_list = []
    sorted_list = []
    n = 0
    feat = ["factor_" + str(i) for i in range(num_factor)]
    user_mat = user_mat[ ['user_id']+feat ]
    item_mat = item_mat[ ['item_id']+feat ]
    for i in range( len(user_mat) ):
        recitems = []
        for j in range( len(item_mat) ):
            predict = user_mat.ix[i,1:].dot( item_mat.ix[j,1:] )
            addAndSortTopK( [item_mat.ix[j,0],predict],sorted_list )
        for item_predict in sorted_list:
            recitems.append( int(item_predict[0]) )
        sorted_list.clear()
        user_list.append( user_mat.ix[i,0] )
        rec_items_list.append( " ".join( map(str,recitems) ) )
        n += 1
        if( n%2==0 ):print(' rec users '+str( n ))
    rec['user_id'] = user_list
    rec['item_id'] = rec_items_list
    del item_all
    del user
    del item
    del user_list
    del rec_items_list
    gc.collect()

    print('过滤掉用户已经看过的')
    user_viewed = pd.DataFrame()
    user_list = []
    viewed_item = []
    for user, group in train[['user_id', 'item_id']].groupby(['user_id'], as_index=False):
        user_list.append(user)
        viewed_item.append(" ".join(  map( str, map( int,list(group['item_id'].unique())) )))
    user_viewed['user_id'] = user_list
    user_viewed['item_id'] = viewed_item
    del user_list
    del viewed_item
    gc.collect()
    rec = pd.merge(rec, user_viewed, how='left', on='user_id').fillna("")
    rec['item_id'] = rec['item_id_x'] + "," + rec['item_id_y']
    rec['item_id'] = rec['item_id'].apply(help)
    rec = rec[['user_id', 'item_id']]
    rec.drop_duplicates('user_id').to_csv('../result/result.csv', index=None, header=None)


if __name__ == '__main__':
    make_train_test()
    exit_num = os.system("../bins/libMF.sh")
    print(  exit_num >> 8 )
    save_user_mat(35)
    save_item_mat(35)
    make_predict(35)