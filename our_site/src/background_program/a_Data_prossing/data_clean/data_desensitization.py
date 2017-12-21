'''
Created on 2017年12月20日
数据脱敏到“软件学院脱敏”数据库中
@author: Jack
'''


def doit():
    """
            将students表中的中文字符串改为数字，方便后续处理
    @params
    @return
    """
    from background_program.z_Tools import MyDataBase
    
    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "select * from students where 1=1"
    
    executer.execute(sql)
    db.close()

    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "select * from students where 1=1"
    
    executer.execute(sql)
    db.close()

if __name__ == '__main__':
    doit()
