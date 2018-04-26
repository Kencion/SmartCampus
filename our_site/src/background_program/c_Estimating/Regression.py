'''
Created on 2018年4月25日

@author: Jack
'''


class LogisticRegression():

    def __init__(self):
        from sklearn.linear_model import LogisticRegression
        
        self.estimater = LogisticRegression(
            penalty='l2',
            dual=False,
            tol=0.0001,
            C=1.0,
            fit_intercept=True,
            intercept_scaling=1,
            class_weight=None,
            random_state=None,
            solver='liblinear',
            max_iter=100,
            multi_class='ovr',
            verbose=0,
            warm_start=False,
            n_jobs=1
            )
