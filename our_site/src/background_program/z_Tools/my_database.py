'''
Created on 2017年7月22日
Modified on 2017年11月23日
项目统一数据库连接工具类
@author: jack
'''
from background_program.z_Tools.my_exceptions import my_exception_handler, database_not_found_exception
from  background_program.z_Tools.my_config import get_database_name, get_database_ip, get_database_pwd, get_database_user


class MyDataBase:
    '''
            使用手册：
        db = MyDataBase("DataBaseName")
        executer = db.getExcuter()
        
        executer.execute(sql)
        data = executer.fetchall()
        
        db.close
    '''

    @my_exception_handler
    def __init__(self, database=get_database_name(), ip=get_database_ip(), user=get_database_user(), pwd=get_database_pwd()):
        import pymysql
        try:
            self.db = pymysql.connect(ip, user, pwd, database, charset='utf8')
        except:
            raise database_not_found_exception
        self.cursor = self.db.cursor()
        self.db.autocommit(True)  # 设置每次执行自动提交

    def getConn(self):
        return self.db

    def getExcuter(self):
        return self.cursor

    @my_exception_handler
    def close(self):
        self.cursor.close()
        self.db.close()
