'''
Created on 2018年3月15日

@author: Jack
'''
from sklearn.metrics import explained_variance_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
from sklearn.metrics import r2_score


class regression_evalueter():

    def __init__(self, y_pred, y_true):
        import numpy as np

        self.y_pred = np.array(y_pred)
        self.y_true = np.array(y_true)


class my_explained_variance_score(regression_evalueter):

    def get_evaluate_score(self):
        evaluete_score = explained_variance_score(self.y_true, self.y_pred)
        
        return evaluete_score


class my_mean_absolute_error():

    def get_evaluate_score(self):
        evaluete_score = mean_absolute_error(self.y_true, self.y_pred)
        
        return evaluete_score


class my_mean_squared_error():

    def get_evaluate_score(self):
        evaluete_score = mean_squared_error(self.y_true, self.y_pred)
        
        return evaluete_score


class my_mean_squared_log_error():

    def get_evaluate_score(self):
        evaluete_score = mean_squared_log_error(self.y_true, self.y_pred)
        
        return evaluete_score


class my_median_absolute_error():

    def get_evaluate_score(self):
        evaluete_score = median_absolute_error(self.y_true, self.y_pred)
        
        return evaluete_score


class my_r2_score():

    def get_evaluate_score(self):
        evaluete_score = r2_score(self.y_true, self.y_pred)
        
        return evaluete_score
    

if __name__ == '__main__':
    pass
