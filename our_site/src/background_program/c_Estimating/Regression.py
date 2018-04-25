'''
Created on 2018年4月25日

@author: Jack
'''


class ExtraTrees():

    def __init__(self):
        from sklearn.ensemble import ExtraTreesClassifier
        
        self.estimater = ExtraTreesClassifier(
            n_estimators=10,
            max_depth=None,
            min_samples_split=2,
            random_state=0)

        
class MyDecesionTree():

    def __init__(self, class_weight=None):
        from sklearn import tree
        
        self.estimater = tree.DecisionTreeClassifier(
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
