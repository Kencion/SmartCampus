'''
Created on 2018年1月19日

@author: YHJ
'''
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn import svm, datasets
from background_program.d_Model_evalueting.Config import Config
from background_program.d_Model_evalueting.Select_Params import Select_Params
import sklearn
class Logistic(object):
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
        param_grid = {"penalty": ["l1","l2"],#用于指定惩罚中使用的标准,默认是l2
                  "tol":[0.1,0.01,0.001,0.0001],#容忍停止标准，默认0.0001
                  "C":[1.0,2.0,3.0,5.0,10.0],#默认值：1.0
                  "max_iter":range(100,500,100)#最大迭代次数，默认100
                  }
        gs = GridSearchCV(LogisticRegression(),
                     param_grid=param_grid)
        sp=Select_Params(self.X_train,self.Y_train,gs)
        best_parameters=sp.GSCV()
#         print(best_parameters)
        #调用Config函数将字典类型转换为对应的参数列表
        obj=Config(**best_parameters)
        #根据最佳参数，重新构造estimator
        estimator=LogisticRegression(penalty=obj.penalty,\
                                     tol=obj.tol,C=obj.C,\
                                     max_iter=obj.max_iter
                                     )
        #评估标准还可以完善，目前实现比较简单，选择同一标准衡量即可，scoring参数的调整可以参照scoring参数说明文档
        score1=sp.cross_val_score_model(estimator,self.X_train,self.Y_train,cv=10,scoring="r2")
        score2=sp.cross_validate_model(estimator, self.X_train, self.Y_train,cv=10)
        print((score1+score2)/2)
        return estimator,(score1+score2)/2
if __name__=='__main__':
    iris = datasets.load_iris()
    l=Logistic(iris.data, iris.target)
    l.Calcute_count()
