'''
Created on 2018年4月25日

@author: Jack
'''


class My_Adaboost():

    def __init__(self, base_estimator=None, n_estimators=10):
        from sklearn.ensemble import AdaBoostClassifier  
        
        self.estimater = AdaBoostClassifier(
            base_estimator,
            n_estimators,
            learning_rate=1.0,
            algorithm='SAMME.R',
            random_state=None)


class My_VotingClassifier():

    def __init__(self, estimators=[], weights=None):
        from sklearn.ensemble import VotingClassifier  
        
        self.estimater = VotingClassifier(
            estimators,
            voting='soft',
            weights=weights,
            n_jobs=1,
            flatten_transform=None)
