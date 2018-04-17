'''
Created on 2018年4月17日

@author: YHJ
'''
#模型融合的父类
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_iris
from sklearn.ensemble import AdaBoostClassifier
from background_program.d_Model_evalueting.Config import Config
from sklearn import model_selection
from background_program.d_Model_evalueting.Model_Combine.RandomForest import RandomForest
from background_program.d_Model_evalueting.Model_Combine.DecisionTree import DecisionTree
class ADABOOST():
    def __init__(self,X_train,Y_train):
        self.X_train=X_train
        self.Y_train=Y_train
    #调主函数ADABOOST的参数
    def Adjust_Param(self):
        param_grid = {"n_estimators":range(30, 100, 10),
              "learning_rate": [0.1,0.5,0.6,1.0],
              }
        gs = GridSearchCV(AdaBoostClassifier(random_state=42),
                 param_grid=param_grid)
        gs.fit(self.X_train,self.Y_train)
        best_parameters = gs.best_estimator_.get_params() 
         
        obj=Config(**best_parameters)
        #estimator=AdaBoostClassifier(n_estimators=estimator,learning_rate=obj.learning_rate)
        return obj.n_estimators,obj.learning_rate
     #模型融合
    def Model_Fusion(self):
        #单模型选择
        estimator_RandomForest=RandomForest(self.X_train,self.Y_train).Calcute_count()
        estimator_Tree=DecisionTree(self.X_train,self.Y_train).Calcute_count()
        #主算法的最优参数配置
        n_estimators,learning_rate=self.Adjust_Param()
        clf_RF = AdaBoostClassifier(base_estimator=estimator_RandomForest,algorithm='SAMME',n_estimators=n_estimators,learning_rate=learning_rate) 
        score_RF=model_selection.cross_val_score(clf_RF,self.X_train,self.Y_train,cv=10,scoring="accuracy")
        
        clf_Tree= AdaBoostClassifier(base_estimator=estimator_Tree,n_estimators=n_estimators,learning_rate=learning_rate)
        score_Tree = cross_val_score(clf_Tree, self.X_train, self.Y_train)
        if score_RF.mean()>score_Tree.mean():
            print(score_RF.mean())
            return score_RF.mean()
        else:
            print(score_Tree.mean())
            return score_Tree.mean()
            
if __name__=='__main__':  
    iris = load_iris()
    ada=ADABOOST(iris.data, iris.target)
    ada.Model_Fusion()