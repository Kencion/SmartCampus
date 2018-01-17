'''
Created on 2018年1月16日

@author: YHJ
'''
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score
from sklearn import model_selection
from background_program.d_Model_evalueting.Config import Config
class Select_Params(object):
    def __init__(self,X_train,Y_train,gs):
        self.X_train=X_train
        self.Y_train=Y_train
        self.gs=gs
    """
    使用GSCV实现自动调参
    @Param
    @retrun（返回值解释）dict best_parameters：最佳参数组合的dict
    """
    def GSCV(self):
        self.gs.fit(self.X_train,self.Y_train)
        best_parameters = self.gs.best_estimator_.get_params()
        return best_parameters
    """
            获取算法的得分，如果是scoring=neg_mean_squared_error,使用的是平均方差损失函数,得分越大，效果越差，如果scoring="accuracy"，使用的是准确率评估
    @retrun（返回值解释）results.mean():float:该算法多组得分的平均值
    """
    def cross_val_score_model(self,estimator,X,Y,cv=10,scoring="accuracy"):
        kfold = model_selection.KFold(n_splits=10, random_state=1)
        rkfold=model_selection.RepeatedKFold(n_splits=10, random_state=1)
        results = model_selection.cross_val_score(estimator,X,Y,cv=kfold,scoring="accuracy")#cv一定要有值
        results2 = model_selection.cross_val_score(estimator,X,Y,cv=rkfold,scoring="accuracy")
        return (results.mean()+results2.mean())/2
    def cross_validate_model(self,estimator,X, Y, cv=10):
        kfold = model_selection.KFold(n_splits=10, random_state=1)
        rkfold=model_selection.RepeatedKFold(n_splits=10, random_state=1)
        test_score=model_selection.cross_validate(estimator,X,Y, cv=kfold)
        test_score2=model_selection.cross_validate(estimator,X,Y, cv=rkfold)
        return (test_score['test_score'].mean()+test_score2['test_score'].mean())/2
if __name__=='__main__':
    iris = datasets.load_iris()
    param_grid = {"max_depth": [3,4],
              "max_features": [1, 3],
              "min_samples_split": range(2, 403, 10),
              "min_samples_leaf": [1, 3, 10],
              "criterion": ["gini", "entropy"]
              }
    gs = GridSearchCV(DecisionTreeClassifier(random_state=42),
                 param_grid=param_grid)
    sp=Select_Params(iris.data, iris.target,gs)
    sp.GSCV()