'''
Created on 2017年7月22日
Modified on 2017年11月23日
日志记录器
@author: jack
使用手册在最下面
'''

import sys, logging.config
from Tools.__init__ import get_log_open, get_log_file

class MyLogger:
    '''
    日志类
    '''

    def __init__(self, filename=get_log_file()):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename=filename,
            filemode='a'
        )

    def printLogs(self):
        '''
        输出到屏幕
        :return:
        '''

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)


def logger():
    '''
    测试用例
    :return:
    '''

    logger = MyLogger()
    logger.printLogs()
    logging.debug('This is debug message!')
    logging.info('This is info message!')
    logging.warning('This is warning message!')
    logging.error('This is error message!')


def loggerByConfig():
    '''
    通过读取日志配置文件记载日志
    :return:
    '''
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger('example01')
    logger.debug('This is debug message!')
    logger = logging.getLogger('example02')
    logger.error('This is error message!')

def myException(function):
    '''
    使用手册：
    1.打开日志记录功能，把变量 open 设置为True（本功能可以屏蔽掉一些不必要的error report）
    2.关闭日志记录功能，把变量 open 设置为False（代码有错，程序会立马停止运行）
    
    '''
    def wrapper(*args, **kwargs):
        if get_log_open():
            try:
                return function(*args, **kwargs)
            except:
                logger = MyLogger()
                info = sys.exc_info()
                logging.error(function.__doc__)
                logging.error(str(info[0]) + ":" + str(info[1]))
                print(function.__doc__)
        else:
            return function(*args, **kwargs)
    return wrapper
