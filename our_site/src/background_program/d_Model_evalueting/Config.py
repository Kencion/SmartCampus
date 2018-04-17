'''
Created on 2018年4月17日

@author: YHJ
'''
class Config(object):
    def __init__(self,**entries):
        self.__dict__.update(entries)