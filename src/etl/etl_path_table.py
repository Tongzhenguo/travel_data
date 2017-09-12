import random

import pandas as pd

data = pd.read_csv('../../data/out.csv')[['start_date','days','money','who','pois']]

def get_session( x ):
    month = str(x).strip()
    if month in ['','nan']:
        return '其他'
    month = int(month[4:6])
    if month in [3,4,5]:
        return '3-5月'
    if month in [6,7,8]:
        return '6-8月'
    if month in [9,10,11]:
        return '9-11月'
    if month in [12,1,2]:
        return '12-2月'
    return '其他'

def make_days( row ):
    s = str(row[1]).strip().replace('天','')
    if len(s)==0 or s=='nan':
        row[1] = int(len(str(row[-2]).strip().split('/')) / 3)
    else:
        row[1] = int(s)
    if row[1] in range(1,3):
        row[1] = '1-2天'
        return row
    if row[1] in range(3,6):
        row[1] = '3-5天'
        return row
    if row[1] in range(6,9):
        row[1] = '6-8天'
        return row
    if row[1] in range(9,15):
        row[1] = '9-14天'
        return row
    if int(row[1])>15:
        row[1] = '15天以上'
        return row

def make_money( x ):
    s = str(x).strip()[1:]
    if len(s)>0:
        m = int(s)
    else:
        m = random.randint(0,10000)
    if m<1000:
        return '1000以内'
    if m > 1000 and m < 5000:
        return '1000-5000'
    if m > 5000 and m < 10000:
        return '5000-10000'
    else:
        return '10000以上'

def make_who( x ):
    if x in ('一个人',''):
        return '独行'
    if x == '和朋友':
        return '朋友'
    if x == '和父母':
        return '父母'
    if x in ['情侣','夫妻']:
        return '情侣/夫妻'

data['start_month'] = data['start_date'].apply( get_session )
data['money'] = data['money'].apply( make_money )
data = data.apply(make_days,axis=1)
data['who'] = data['who'].apply( make_who )
data.columns = ['start_date','days','money','who','poi_seq','start_month']
data = data.dropna()
data = data[ data.poi_seq.__len__()>2 ][['start_month','days','money','who','poi_seq']]
data[['start_month','days','money','who','poi_seq']].to_csv('../../data/path.csv',encoding='utf8',header=False,index=False)

'''
DROP TABLE IF EXISTS `mydb`.`path` ;

CREATE TABLE IF NOT EXISTS `mydb`.`path` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `start_month` VARCHAR(45) NULL,
  `days` VARCHAR(45) NULL,
  `money` VARCHAR(45) NULL,
  `who` VARCHAR(45) NULL,
  `poi_seq` VARCHAR(1000) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB
;

LOAD DATA INFILE "/var/lib/mysql-files/path_id.csv"
REPLACE INTO TABLE path
CHARACTER SET utf8
FIELDS TERMINATED BY "," ENCLOSED BY ""
;
'''