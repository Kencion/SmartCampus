'''
Created on 2017年7月22日

@author: zhenglongtian
'''
from c_Estimating.Classification.SingleClassifiers.SingleClassfier import SingleClassifier
from sklearn import tree

class DecesionTree(SingleClassifier):
    def __init__(self, class_weight=None):
        SingleClassifier.__init__(self)
        # weak classifier
        self.clf = tree.DecisionTreeClassifier(
            criterion='gini',
            splitter='best',
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.0,
            max_features=None,
            random_state=None,
            max_leaf_nodes=None,
            min_impurity_split=0.0,
            class_weight=class_weight,
            presort=True
            )
