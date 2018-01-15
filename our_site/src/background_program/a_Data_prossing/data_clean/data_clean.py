'''
Created on 2017年11月27日
把students表中的字符串字段改为数据
@author: Jack
'''


def doit():
    """
            将students表中的中文字符串改为数字，方便后续处理
    @params
    @return
    """
    from background_program.z_Tools.my_database import MyDataBase
    
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = ""
    with open('data_clean.sql', 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            print(sql)
            sql = sql + line
    
    executer.execute(sql)
    db.close()


if __name__ == '__main__':
    doit()
