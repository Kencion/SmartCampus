'''
Created on 2017年7月22日

@author: zhenglongtian
'''
from sklearn.ensemble import ExtraTreesClassifier

class ExtraTrees():
    def __init__(self):
        # weak classifier
        self.clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
