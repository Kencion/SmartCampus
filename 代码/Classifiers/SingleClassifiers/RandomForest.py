'''
Created on 2017年7月22日

@author: zhenglongtian
'''
from __init__ import SingleClassifier
from sklearn.ensemble import RandomForestClassifier

class RandomForest(SingleClassifier):
    def __init__(self):
        SingleClassifier.__init__(self)
        #weak classifier
        self.clf=RandomForestClassifier(random_state=1)
