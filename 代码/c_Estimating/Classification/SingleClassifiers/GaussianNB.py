'''
Created on 2017年7月22日

@author: zhenglongtian
'''
from c_Estimating.Classification.SingleClassifiers.SingleClassfier import SingleClassifier
from sklearn.naive_bayes import GaussianNB

class GaussianNB(SingleClassifier):
    def __init__(self):
        SingleClassifier.__init__(self)
        #weak classifier
        self.clf=GaussianNB()
