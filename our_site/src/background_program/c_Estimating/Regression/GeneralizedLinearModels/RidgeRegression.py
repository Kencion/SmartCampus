'''
Created on 2017年12月13日

@author: LI
'''
class RidgeRegression():
    def __init__(self):
        from sklearn import linear_model

        self.estimater =  linear_model.Ridge(
            alpha=1.0,
            ﬁt_intercept=True,
            normalize=False, 
            copy_X=True, 
            max_iter=None, 
            tol=0.001, 
            solver='auto', 
            random_state=None
            )