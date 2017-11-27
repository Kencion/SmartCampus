'''
Created on 2017年7月22日

@author: zhenglongtian
'''
from Classifiers.SingleClassifiers.SingleClassfier import SingleClassifier
from sklearn import tree

class DecesionTree(SingleClassifier):
    def __init__(self):
        SingleClassifier.__init__(self)
        # weak classifier
        self.clf = tree.DecisionTreeClassifier()
