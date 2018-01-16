'''
Created on 2017年11月29日
选出头K个最好的特诊
@author: Jack
'''

class MySelectKBset():
    
    def __init__(self):
        from sklearn.feature_selection import SelectKBest 
        
        self.selector = SelectKBest(k=10)
