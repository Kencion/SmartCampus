'''
Created on 2018年3月15日

@author: Jack
'''


class accuracy_score():
    
    def __init__(self, y_true, y_pred):
        from sklearn.metrics import accuracy_score
        self.evaluate_score = accuracy_score(y_true, y_pred)
    
    def get_evaluate_score(self):
        return self.evaluate_score

        
class average_precision_score():
    from sklearn.metrics import average_precision_score

    def __init__(self, y_true, y_pred):
        pass


class f1_score():
    from sklearn.metrics import f1_score

    def __init__(self, y_true, y_pred):
        f1_score(y_true, y_pred, average='macro')  
        f1_score(y_true, y_pred, average='micro')  
        f1_score(y_true, y_pred, average='weighted') 
        f1_score(y_true, y_pred, average=None)

            
class log_loss():
    from sklearn.metrics import log_loss

    def __init__(self, y_true, y_pred):
        pass


class precision_score():
    from sklearn.metrics import precision_score

    def __init__(self, y_true, y_pred):
        pass


class recall_score():

    def __init__(self, y_true, y_pred):
        from sklearn.metrics import recall_score
        self.evaluate_score = recall_score(y_true, y_pred)
    
    def get_evaluate_score(self):
        return self.evaluate_score


class roc_auc_score():
    from sklearn.metrics import roc_auc_score

    def __init__(self, y_true, y_pred):
        pass
