ctrip_cnt = 4673
import pandas as pd

data = pd.read_csv('../../data/数据集2_用户标签.csv',encoding='gbk')[["用户标识","性别","年龄段","大致消费水平","漫出省份"]]
data = data.dropna()
data['strategy_index'] = data['用户标识'].apply( lambda x:int(x[2:]) % ctrip_cnt )
data['province'] = data['漫出省份'].apply( lambda x:str(x).split(',')[0] )
data = data[['strategy_index',"性别","年龄段",'province',"大致消费水平"]]
data.columns = ['strategy_index',"sex","age",'province',"cost_level"]
for i in ["sex","age","cost_level"]:
    data[i] = data[i].astype(int)
data = data[ (data['sex']!=2) & (data['age']!=0) & (data['cost_level']!=0) & (data['province']!='无') ]
data.to_csv('../../data/user.csv',encoding='utf8',index=False)

'''
DROP TABLE IF EXISTS `mydb`.`user` ;

CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `strategy_index` INT NULL,
  `sex` INT NULL,
  `age` INT NULL,
  `province` VARCHAR(45) NULL,
  `cost_level` INT NULL
  )
ENGINE = InnoDB
KEY_BLOCK_SIZE = 4;

LOAD DATA INFILE "/var/lib/mysql-files/user.csv"
REPLACE INTO TABLE user
CHARACTER SET utf8
FIELDS TERMINATED BY "," ENCLOSED BY ""
;
'''