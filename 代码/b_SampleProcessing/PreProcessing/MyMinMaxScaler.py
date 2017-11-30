'''
Created on 2017年11月30日
将特征缩放到一个范围
@author: Jack
'''

class MyMinMaxScaler():
    def __init__(self):
        from sklearn.preprocessing import MinMaxScaler
        self.transformer = MinMaxScaler(
            feature_range=(0, 5),
            copy=False)
