'''
Created on 2017年11月27日
把students表中的字符串字段改为数据
@author: Jack
'''
from Tools import MyDataBase
from tqdm import tqdm


db = MyDataBase.MyDataBase("软件学院")
executer = db.getExcuter()
sql = ""
with open('toNum', 'r', encoding='UTF-8') as f:
    for line in f:
        sql += line

executer.execute(sql)
db.close()
