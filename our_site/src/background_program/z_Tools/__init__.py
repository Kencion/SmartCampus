'''
这边放一些经常用得到的工具
Created on 2017年11月27日
配置文件
@author: Jack
'''

# 项目会用到的一些工具类
__all__ = ['DataCarer', 'MyDataBase', 'MyLogger', 'get_log_open', 'get_log_file', 'get_database_name', 'get_database_ip', 'get_database_user', 'get_database_pwd', ]

# config:

def get_log_open():
    return False

def get_log_file():
    return "/log.log"

def get_database_name():
    return "软件学院"

def get_database_ip ():
    return "172.16.20.5"

def get_database_user ():
    return "root"

def get_database_pwd ():
    return ""
