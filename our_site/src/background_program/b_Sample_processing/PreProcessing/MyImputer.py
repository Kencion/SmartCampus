'''
Created on 2017年11月30日
填补缺失的数据
@author: Jack
'''
class MyImputer():
    
    def __init__(self):
        from sklearn.preprocessing import Imputer
        self.transformer=Imputer(
            missing_values='NaN',
            strategy='mean',
            axis=0,
            verbose=0,
            copy=True)
