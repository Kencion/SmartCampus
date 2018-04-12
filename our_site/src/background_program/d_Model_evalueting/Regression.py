'''
Created on 2018年3月15日

@author: Jack
'''


class adjusted_mutual_info_score():
    from sklearn.metrics import explained_variance_score

    def __init__(self, y_pred, y_true):
        pass
    
    def get_evaluate_score(self):
        return 0


class mean_absolute_error():
    from sklearn.metrics import mean_absolute_error

    def __init__(self, y_pred, y_true):
        pass

    def get_evaluate_score(self):
            return 0


class mean_squared_error():
    from sklearn.metrics import mean_squared_error

    def __init__(self, y_pred, y_true):
        pass

    def get_evaluate_score(self):
        return 0


class mean_squared_log_error():
    from sklearn.metrics import mean_squared_log_error

    def __init__(self, y_pred, y_true):
        pass

    def get_evaluate_score(self):
        return 0


class median_absolute_error():
    from sklearn.metrics import median_absolute_error

    def __init__(self, y_pred, y_true):
        pass

    def get_evaluate_score(self):
        return 0


class r2_score():
    from sklearn.metrics import r2_score

    def __init__(self, y_pred, y_true):
        pass
    
    def get_evaluate_score(self):
        return 0
