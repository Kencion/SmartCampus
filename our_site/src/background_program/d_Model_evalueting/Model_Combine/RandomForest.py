'''
Created on 2018年4月17日

@author:YHJ
'''
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn import svm, datasets
from sklearn.ensemble import RandomForestClassifier
from background_program.d_Model_evalueting.Config import Config
from background_program.d_Model_evalueting.Model_Combine.Select_Params import Select_Params
import sklearn
class RandomForest(object):
    def __init__(self,X_train,Y_train):
        self.X_train=X_train
        self.Y_train=Y_train
    """
        计算各个算法的得分表现
    @retrun（返回值解释）score float 该算法的最后得分，根据得分高低评估该算法对预测的表现
    estimator 经过调整后较优的构造器
    """
    def Calcute_count(self):
        #对应算法需要调整的参数列表
        param_grid = {"n_estimators": range(5,50,5),#森林里的树木数量：默认10
                  "criterion": ["entropy","gini"],#测量分裂质量的函数默认=“gini”   
                  }
        gs = GridSearchCV(RandomForestClassifier(random_state=42),
                     param_grid=param_grid)
        sp=Select_Params(self.X_train,self.Y_train,gs)
        best_parameters=sp.GSCV()
#         print(best_parameters)
        #调用Config函数将字典类型转换为对应的参数列表
        obj=Config(**best_parameters)
        #根据最佳参数，重新构造estimator
        estimator=RandomForestClassifier(n_estimators=obj.n_estimators,criterion=obj.criterion)
        #评估标准还可以完善，目前实现比较简单，选择同一标准衡量即可，scoring参数的调整可以参照scoring参数说明文档
        score1=sp.cross_val_score_model(estimator,self.X_train,self.Y_train,cv=10,scoring="accuracy")
        #score2=sp.cross_validate_model(estimator, self.X_train, self.Y_train,cv=10)
#         print(estimator)
#         print(score1)
        return estimator
if __name__=='__main__':
    iris = datasets.load_iris()
    l=RandomForest(iris.data, iris.target)
    l.Calcute_count()