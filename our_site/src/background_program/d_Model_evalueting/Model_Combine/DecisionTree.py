'''
Created on 2018年4月17日

@author: YHJ
'''
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn import svm, datasets
from sklearn.tree import DecisionTreeClassifier
from background_program.d_Model_evalueting.Config import Config
from background_program.d_Model_evalueting.Model_Combine.Select_Params import Select_Params
import sklearn
class DecisionTree(object):
    def __init__(self,X_train,Y_train):
        self.X_train=X_train
        self.Y_train=Y_train
    def Calcute_count(self):
        #对应算法需要调整的参数列表
        param_grid = {"max_depth": [1,2,4],
                  "max_features": [1, 3],
                  "min_samples_split": range(2, 403, 10),
                  "min_samples_leaf": [1, 3, 10],
                  "criterion": ["gini", "entropy"]
                  }
        gs = GridSearchCV(DecisionTreeClassifier(random_state=42),
                     param_grid=param_grid)
        sp=Select_Params(self.X_train,self.Y_train,gs)
        best_parameters=sp.GSCV()
        #调用Config函数将字典类型转换为对应的参数列表
        obj=Config(**best_parameters)
        #根据最佳参数，重新构造estimator
        estimator=DecisionTreeClassifier(criterion=obj.criterion,max_depth=obj.max_depth,\
                                         min_samples_split=obj.min_samples_split,min_samples_leaf=obj.min_samples_leaf,\
                                         max_features=obj.max_features)
        #score1=sp.cross_val_score_model(estimator,self.X_train,self.Y_train,cv=10,scoring="accuracy")
        #score2=sp.cross_validate_model(estimator, self.X_train, self.Y_train,cv=10,return_train_score="False")
#         print((score1+score2)/2)
        return estimator
if __name__=='__main__':
    iris = datasets.load_iris()
    l=DecisionTree(iris.data, iris.target)
    l.Calcute_count() 