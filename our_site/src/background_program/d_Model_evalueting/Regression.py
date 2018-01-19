'''
Created on 2017年12月28日

@author: YHJ
'''
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
class Regression(FeatureCalculater):
    "将训练集传进来，包括标签,Y_train表示标签列"
    def __init__(self,X_train,Y_train):
        self.X=X_train
        self.Y=Y_train
        """
                            模型参数配置，调参
        @retrun（返回值解释）model:list;调参后的模型            
        """
    def build_model(self):
        model=[]
        model.append(SVR(kernel='rbf',degree=3,gamma='auto',coef0=0.0,tol=0.001,C=1.0,epsilon=0.1,shrinking=True,cache_size=200,verbose=False,max_iter=-1))
        model.append(DecisionTreeRegressor(criterion='mse',splitter='best',max_depth=None,min_samples_split=2,min_samples_leaf=1,min_weight_fraction_leaf=0.0,max_features=None,random_state=None,max_leaf_nodes=None,min_impurity_decrease=0.0,min_impurity_split=None,presort=False))
        model.append(KNeighborsRegressor(n_neighbors=5,weights='uniform',algorithm='auto',leaf_size=30,p=2,metric='minkowski'))
        model.append(Lasso(alpha = 1.0,fit_intercept = True,normalize = False,precompute = False,copy_X = True,max_iter = 1000,tol = 0.0001,warm_start = False,positive = False ))
        model.append(LinearRegression(fit_intercept = False,normalize = True,copy_X = True,n_jobs = 1 ))
        model.append(Ridge(alpha=30.0,fit_intercept=False,copy_X=True,max_iter=None,tol=0.1,solver='auto'))
        model.append(ElasticNet(alpha = 1.0,l1_ratio = 0.5,fit_intercept = True,normalize = False,precompute = False,max_iter = 1000,copy_X = True,tol = 0.0001,warm_start = False,positive = False,random_state = None,selection ='cyclic'))
        return model
    """
            获取算法的得分，如果是scoring=neg_mean_squared_error,使用的是平均方差损失函数,得分越大，效果越差，如果scoring="accuracy"，使用的是准确率评估
    @retrun（返回值解释）results.mean():float:该算法多组得分的平均值
    """
    def cross_val_score_model(self,model_name,X,Y,cv,scoring="neg_mean_squared_error"):
        results = -1*model_selection.cross_val_score(model_name, X, Y, cv, scoring)#通过交叉验证生成模型得分 
        print(str(model_name)+"kfold_cross_val_score:%s"%results.mean())
        return results.mean()
    def cross_validate_model(self,model_name,X, Y, cv,return_train_score=False):
        test_score=model_selection.cross_validate(model_name, X, Y, cv,return_train_score=False)
        print("kfold_cross_validate:%s"%test_score['test_score'].mean())#得分越高越好
        return test_score['test_score'].mean()
    """
            计算各个算法的得分表现
    @Param num：int需要选择的算法个数 
    @retrun（返回值解释）dic list：[('算法名称', 得分),]
    """
    def calcute(self,num):
        scoring = 'mean_squared_error'#使用的是平均方差损失函数，accuracy使用的是准确率评估
        seed=7
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        rkfold=model_selection.RepeatedKFold(n_splits=10, random_state=seed)
        dic={}
        models=self.build_model()
        for model_name in models:
            kf_cross_val_score= self.cross_val_score_model(model_name, self.X, self.Y, cv=kfold, scoring=scoring)#通过交叉验证生成模型得分 
            kf_cross_validate_of_score=self.cross_validate_model(model_name, self.X, self.Y, cv=kfold,return_train_score=False)
            
            rkf_cross_val_score = self.cross_val_score_model(model_name, self.X, self.Y, cv=rkfold, scoring=scoring)
            rkf_cross_validate_of_score=self.cross_validate_model(model_name, self.X, self.Y, cv=rkfold,return_train_score=False)
            score=kf_cross_val_score*0.25+kf_cross_validate_of_score*0.25+rkf_cross_val_score*0.25+rkf_cross_validate_of_score*0.25
            dic[model_name]=score
        dic=sorted(dic.items(),key=lambda item:item[1],reverse=True)#返回根据得分排序后的list,升序
        count=0
        for d in range(len(dic)):
            if count>=num:
                del dic[d]
                count+=1
        return dic

