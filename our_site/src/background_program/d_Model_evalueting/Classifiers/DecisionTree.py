'''
Created on 2018年1月17日

@author: YHJ
'''
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from background_program.d_Model_evalueting.Config import Config
from background_program.d_Model_evalueting.Select_Params import Select_Params


class DecisionTree(object):

    def __init__(self, X_train, Y_train):
        self.X_train = X_train
        self.Y_train = Y_train

    def Calcute_count(self):
        """
        x计算各个算法的得分表现
        @retrun（返回值解释）score float 该算法的最后得分，根据得分高低评估该算法对预测的表现
        """
        # 对应算法需要调整的参数列表
        param_grid = {"max_depth": [1, 2, 4],
                  "max_features": [1, 3],
                  "min_samples_split": range(2, 403, 10),
                  "min_samples_leaf": [1, 3, 10],
                  "criterion": ["gini", "entropy"]
                  }
        gs = GridSearchCV(DecisionTreeClassifier(random_state=42),
                     param_grid=param_grid)
        sp = Select_Params(self.X_train, self.Y_train, gs)
        best_parameters = sp.GSCV()
        # 调用Config函数将字典类型转换为对应的参数列表
        obj = Config(**best_parameters)
        # 根据最佳参数，重新构造estimator
        estimator = DecisionTreeClassifier(criterion=obj.criterion, max_depth=obj.max_depth, \
                                         min_samples_split=obj.min_samples_split, min_samples_leaf=obj.min_samples_leaf, \
                                         max_features=obj.max_features)
        # 评估标准还可以完善。。。。
        score1 = sp.cross_val_score_model(estimator, self.X_train, self.Y_train, cv=10, scoring="accuracy")
        score2 = sp.cross_validate_model(estimator, self.X_train, self.Y_train, cv=10, return_train_score="False")
        print((score1 + score2) / 2)
        return (score1 + score2) / 2
