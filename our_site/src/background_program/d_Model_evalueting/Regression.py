'''
Created on 2018年3月15日

@author: Jack
'''


class adjusted_mutual_info_score():

    def __init__(self, y_pred, y_true):
        from sklearn.metrics import explained_variance_score
        self.evaluate_score = explained_variance_score(y_pred, y_true)
    
    def get_evaluate_score(self):
        return self.evaluate_score


class mean_absolute_error():

    def __init__(self, y_pred, y_true):
        from sklearn.metrics import mean_absolute_error
        self.evaluate_score = mean_absolute_error(y_pred, y_true)
    
    def get_evaluate_score(self):
        return self.evaluate_score


class mean_squared_error():

    def __init__(self, y_pred, y_true):
        from sklearn.metrics import mean_squared_error
        self.evaluate_score = mean_squared_error(y_pred, y_true)
    
    def get_evaluate_score(self):
        return self.evaluate_score


class mean_squared_log_error():

    def __init__(self, y_pred, y_true):
        from sklearn.metrics import mean_squared_log_error
        self.evaluate_score = mean_squared_log_error(y_pred, y_true)
    
    def get_evaluate_score(self):
        return self.evaluate_score


class median_absolute_error():

    def __init__(self, y_pred, y_true):
        from sklearn.metrics import median_absolute_error
        self.evaluate_score = median_absolute_error(y_pred, y_true)
    
    def get_evaluate_score(self):
        return self.evaluate_score


class r2_score():

    def __init__(self, y_pred, y_true):
        from sklearn.metrics import r2_score
        self.evaluate_score = r2_score(y_pred, y_true)
    
    def get_evaluate_score(self):
        return self.evaluate_score
