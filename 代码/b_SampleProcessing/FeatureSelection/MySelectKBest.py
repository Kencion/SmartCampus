'''
Created on 2017年11月29日
选出头K个最好的特诊
@author: Jack
'''
from sklearn.feature_selection import SelectKBest 

class MySelectKBset():
    
    def __init__(self):
        self.selector = SelectKBest(k=10)