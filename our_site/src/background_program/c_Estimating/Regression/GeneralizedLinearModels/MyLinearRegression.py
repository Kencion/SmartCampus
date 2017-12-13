'''
Created on 2017年12月12日

@author: LI
'''
class MyLinearRegression():
    def __init__(self):
        from sklearn import linear_model

        
        self.estimater =  linear_model.LinearRegression(
            ﬁt_intercept=True, 
            normalize=False, 
            copy_X=True, 
            n_jobs=3
            )
