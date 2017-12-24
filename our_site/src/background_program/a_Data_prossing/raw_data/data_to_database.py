'''
Created on 2017年11月30日

@author: Jack
'''
def dataToDataBase():
    from background_program.z_Tools import MyDataBase
    
    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = ""
    with open('软件学院.sql', 'r', encoding='UTF-8') as f:
        for line in f:
            sql += line
    
    executer.execute(sql)
    db.close()