'''
Created on 2017年12月28日

@author: YHJ
'''
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
from sklearn import model_selection
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
class Classifier(FeatureCalculater):
    "将训练集传进来，包括标签,Y_train表示标签列"
    def __init__(self,X_train,Y_train):
        self.X=X_train
        self.Y=Y_train
    def build_model(self):
        model=[]
        model.append(DecisionTreeClassifier(criterion='gini',splitter='best', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, random_state=None, max_leaf_nodes=None, min_impurity_decrease=0.0, min_impurity_split=None, class_weight=None, presort=False))
        model.append(SVC(C=1.0,kernel='rbf',degree=3,gamma='auto',coef0=0.0,shrinking=True,probability=False,tol=0.001,cache_size=200,class_weight=None,verbose=False,max_iter=-1,random_state=None))
        model.append(MLPClassifier(hidden_layer_sizes=(100,),activation='relu',solver='adam',alpha=0.0001,batch_size='auto',learning_rate='constant',learning_rate_init=0.001,power_t=0.5,max_iter=200,shuffle=True,random_state=None,tol=0.0001,verbose=False,warm_start=False,momentum=0.9,nesterovs_momentum=True,early_stopping=False,validation_fraction=0.1,beta_1=0.9,beta_2=0.999,epsilon=1e-08))
        model.append(RandomForestClassifier(n_estimators=10,criterion='gini',max_depth=None,min_samples_split=2,min_samples_leaf=1,min_weight_fraction_leaf=0.0,max_features='auto',max_leaf_nodes=None,min_impurity_decrease=0.0,min_impurity_split=None,bootstrap=True,oob_score=False,n_jobs=1,random_state=None,verbose=0,warm_start=False,class_weight=None))
        return model
    def cross_val_score_model(self,model_name,X,Y,cv,scoring="f1_samples"):
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