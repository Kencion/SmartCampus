'''
Created on 2017年11月29日
选取前百分percentile的特征
@author: Jack
'''

class MySelectPercentile():
    
    def __init__(self):
        from sklearn.feature_selection import SelectPercentile
         
        self.selector =  SelectPercentile(percentile=50)
