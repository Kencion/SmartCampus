'''
Created on 2017年11月29日
选取前百分percentile的特征
@author: Jack
'''
from sklearn.feature_selection import SelectPercentile 

class MySelectPercentile():
    
    def __init__(self):
        self.selector = SelectPercentile(percentile=50)