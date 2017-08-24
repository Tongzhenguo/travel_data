# coding=utf-8
import os
import random
import gc
import pandas as pd
import time
import pickle
from sklearn.model_selection import train_test_split
import xgboost as xgb

"""
    点击率预测模型，用于最后候选集的rerank
"""

def randomSelectTrain( train,start,end ):
    '''
    随机收取负样本
    '''
    path = '../cache/train_{st}_{ed}.pkl'.format( st=start,ed=end )
    if os.path.exists( path ):
        data = pickle.load(open(path, "rb"))
    else:
        data = pd.DataFrame()
        user_list = []
        item_list = []
        label_list = []
        items_pool = list(train['item_id'].values)
        rec = dict()
        print('recent k items')
        train = train.sort_values(['action_time'],ascending=False)[['user_id','item_id']].drop_duplicates()
        for user, group in train.groupby(['user_id'],sort=False):
            viewed_item = list( group['item_id'].head(5).values )
            for item in viewed_item:
                rec[item] = 1
                user_list.append(user)
                item_list.append(item)
                label_list.append(1)
            n = 0
            for i in range( 0, len(items_pool) ):
                item = items_pool[random.randint(0, len(items_pool) - 1)]
                if item in rec.keys():
                    continue
                user_list.append(user)
                item_list.append(item)
                label_list.append(0)
                n += 1
                rec[item] = 0
                if n > len(viewed_item):
                    break
            rec.clear()
        data['user_id'] = user_list
        data['item_id'] = item_list
        data['label'] = label_list
        del user_list
        del item_list
        del label_list
        gc.collect()
        pickle.dump( data,open(path,'wb'),True )
    return data

def show_user_cate(train):
    cate_list = list( train['cate_id'].unique() )
    cate_list.sort()
    train = train[['user_id', 'cate_id', 'action_type']].groupby(['user_id', 'cate_id']).count().unstack().fillna(0)
    train.columns = ["cate_" + cate_id for cate_id in cate_list]
    train = train.reset_index()
    return train

def user_action_count(user ):
    train = pd.read_csv('../data/train.csv')
    train = pd.merge(train,user,on='user_id')
    train = train[['user_id','action_type','action_time']].groupby(['user_id','action_type']).count().unstack().fillna(0)
    train.columns = [str(type)+'_count' for type in ['view','deep_view','share','comment','collect'] ]
    train = train.reset_index()
    return train

def get_item_action_count( train ):
    train = train[[ 'item_id','user_id' ]].groupby( ['item_id'],as_index=False ).count()
    train.columns = ['item_id','action_count']
    return train

def get_action_weight( x):
    pass

def make_train_set():
    pass

def make_test_data():
    pass

def xgb_train( ):
    i = 0
    print('=========================training==============================')
    index,label,data = make_train_set(  )
    X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=1990)
    # see how many neg/pos sample
    label = label.values
    print( "neg:{0},pos:{1}".format(len(label[label == 0]), len(label[label == 1])) )
    # scale_pos_weight = (len(label[label == 0])) / float(len(label[label == 1]))
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)
    param = {'max_depth': 3,
             'min_child_weight': 2,
             'gamma': 0,
             'subsample': 1.0,
             'colsample_bytree': 0.8,
              'eta': 0.1,
             'lambda': 5,  # L2惩罚系数
             'scale_pos_weight': 56/3,
             'objective': 'binary:logistic',
             'eval_metric': 'auc',
             'early_stopping_rounds': 50,  # eval 得分没有继续优化 就停止了
             'seed': 1990,
             'nthread': 4,
             'silent': 0
             }
    evallist = [(dtest, 'eval'), (dtrain, 'train')]
    bst = xgb.train(param, dtrain, num_boost_round=500, evals=evallist)

    bst.save_model(os.path.join('../model', ('xgb%02d.model' % i)))
    print('save feature score and feature information')
    feature_score = bst.get_fscore()
    for key in feature_score:
        feature_score[key] = [feature_score[key]]
    feature_score = sorted(feature_score.items(), key=lambda x: x[1], reverse=True)
    fs = []
    for (key, value) in feature_score:
        fs.append("{0},{1}\n".format(key, value))
    if not os.path.exists('../data/features'):
        os.mkdir('../data/features')

    fpath = os.path.join('../data/features', 'feature_score%02d.csv' % i)
    with open(fpath, 'w') as f:
        f.writelines("feature,score\n")
        f.writelines(fs)


def xgb_sub(  ):
    i = 0
    bst = xgb.Booster({'nthread': 4})  # init model
    bst.load_model( '../model/xgb%02d.model' % i )  # load data

    print('开始构造测试集---------------------------------------------------')
    sub_index, sub_trainning_data = make_test_data()
    test = xgb.DMatrix(sub_trainning_data)
    sub_index['score'] = bst.predict(test)
    sub_index = sub_index.sort_values( ['user_id','score'],ascending=False )
    rec = pd.DataFrame()
    user_list = []
    rec_items_list = []
    for user,group in sub_index.groupby( ['user_id'],as_index=False,sort=False ):
        rec_items = " ".join(map(str, list(group['item_id'].head(5).values)))
        user_list.append(user)
        rec_items_list.append(rec_items)
    rec['user_id'] = user_list
    rec['item_id'] = rec_items_list

    rec = rec.drop_duplicates('user_id')
    rec.to_csv('../result/result_xgb.csv', index=None,header=None)

if __name__ == '__main__':
    xgb_train()
    xgb_sub()