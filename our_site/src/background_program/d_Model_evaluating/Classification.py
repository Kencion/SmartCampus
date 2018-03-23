'''
Created on 2018年3月15日

@author: Jack
'''


class accuracy_score():
    from sklearn.metrics import accuracy_score

    def __init__(self, y_pred, y_true):
        pass
    
    def xx(self):
        y_pred = [0, 2, 1, 3]
        y_true = [0, 1, 2, 3]
        print(accuracy_score(y_true, y_pred))
        
        print(accuracy_score(y_true, y_pred, normalize=False))

        
class average_precision_score():
    from sklearn.metrics import average_precision_score

    def __init__(self, y_pred, y_true):
        pass


class f1_score():
    from sklearn.metrics import f1_score

    def __init__(self, y_pred, y_true):
        f1_score(y_true, y_pred, average='macro')  
        f1_score(y_true, y_pred, average='micro')  
        f1_score(y_true, y_pred, average='weighted') 
        f1_score(y_true, y_pred, average=None)

            
class log_loss():
    from sklearn.metrics import log_loss

    def __init__(self, y_pred, y_true):
        pass


class precision_score():
    from sklearn.metrics import precision_score

    def __init__(self, y_pred, y_true):
        pass


class recall_score():
    from sklearn.metrics import recall_score

    def __init__(self, y_pred, y_true):
        pass


class roc_auc_score():
    from sklearn.metrics import roc_auc_score

    def __init__(self, y_pred, y_true):
        pass
