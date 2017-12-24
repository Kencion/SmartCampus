'''
Created on 2017年7月22日
Modified on 2017年11月23日
项目统一数据库连接工具类
@author: jack
'''
import pymysql
from  background_program.z_Tools.__init__ import get_database_name, get_database_ip, get_database_pwd, get_database_user

class MyDataBase:
    '''
            使用手册：
        db = MyDataBase("DataBaseName")
        executer = db.getExcuter()
        
        executer.execute(sql)
        data = executer.fetchall()
        
        db.close
    '''
    def __init__(self, database=get_database_name(), ip=get_database_ip(), user=get_database_user(), pwd=get_database_pwd()):
#         print("connect to data base " + database + " ......")
        self.db = pymysql.connect(ip, user, pwd, database, charset='utf8')
        self.cursor = self.db.cursor()
        self.db.autocommit(True)  # 设置每次执行自动提交
#         print("connect success!")

    def getConn(self):
        return self.db

    def getExcuter(self):
        return self.cursor

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    print("a module used to connect db")
    t = MyDataBase()
    t.close()
