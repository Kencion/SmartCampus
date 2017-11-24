'''
Created on 2017年7月22日

@author: zhenglongtian
'''
from __init__ import SingleClassifier
from sklearn.naive_bayes import GaussianNB

class GaussianNB(SingleClassifier):
    def __init__(self):
        SingleClassifier.__init__(self)
        #weak classifier
        self.clf=GaussianNB()
