'''
Created on 2018年4月25日

@author: Jack
'''


class My_Cart():

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


class My_ID3():

    def __init__(self, class_weight=None):
        from sklearn import tree
        
        self.estimater = tree.DecisionTreeClassifier(
            criterion='entropy',
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

class My_C4_5():

    def __init__(self, class_weight=None):
        from sklearn import tree
        
        self.estimater = tree.DecisionTreeClassifier(
            criterion='entropy',
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


class My_ExtraTrees():

    def __init__(self):
        from sklearn.ensemble import ExtraTreesClassifier
        
        self.estimater = ExtraTreesClassifier(
            n_estimators=10,
            max_depth=None,
            min_samples_split=2,
            random_state=0)


class My_SVM():

    def __init__(self, class_weight=None):
        from sklearn import svm
        
        self.estimater = svm.SVC(
            C=1.0,
            cache_size=200,
            class_weight=class_weight,  # {class_label : value} 
            coef0=0.0,
            decision_function_shape='ovr',
            degree=3,
            gamma='auto',
            kernel='rbf',
            max_iter=-1,
            probability=False,
            random_state=None,
            shrinking=True,
            tol=0.001,
            verbose=False)


class My_GaussianNB():

    def __init__(self):
        from sklearn.naive_bayes import GaussianNB  
        
        self.estimater = GaussianNB()


class My_MultinomialNB():

    def __init__(self):
        from sklearn.naive_bayes import MultinomialNB  
        
        self.estimater = MultinomialNB()


class My_BernoulliNB():

    def __init__(self):
        from sklearn.naive_bayes import BernoulliNB  
        
        self.estimater = BernoulliNB()

        
class My_Adaboost():

    def __init__(self):
        from sklearn.naive_bayes import BernoulliNB  
        
        self.estimater = BernoulliNB()
