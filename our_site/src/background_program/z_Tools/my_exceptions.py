'''
Created on 2017年12月24日

@author: Jack
'''
import sys, logging.config
from background_program.z_Tools.my_config import get_log_open, get_log_file


class feature_null_exception(Exception):
    pass


class database_not_found_exception(Exception):
    pass


def my_exception_handler(function):
    '''
            使用手册：
    logger = MyLogger()
    logger.printLogs()
    logging.debug('This is debug message!')
    logging.info('This is info message!')
    logging.warning('This is warning message!')
    logging.error('This is error message!')
    
    logging.config.fileConfig('logger.conf')
    logger = logging.getLogger('example01')
    logger.debug('This is debug message!')
    logger = logging.getLogger('example02')
    logger.error('This is error message!')
    1.打开日志记录功能，把变量 open 设置为True（本功能可以屏蔽掉一些不必要的error report）
    2.关闭日志记录功能，把变量 open 设置为False（代码有错，程序会立马停止运行）
    
    '''

    def wrapper(*args, **kwargs):
        if get_log_open():
            try:
                return function(*args, **kwargs)
            except feature_null_exception:
                pass
            except:
                info = sys.exc_info()
                logging.error(function.__doc__)
                logging.error(str(info[0]) + ":" + str(info[1]))
                print(function.__doc__)
        else:
            return function(*args, **kwargs)

    return wrapper
