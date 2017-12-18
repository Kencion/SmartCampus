'''
Created on 2017年12月17日

@author: LI
'''
import sys
from sklearn.model_selection import cross_val_score
from sklearn.metrics import *
import numpy as np
from background_program.b_SampleProcessing.Dimension_Reduction.MyPca import MyPca
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion
class score_forcasting():
    
    def __init__(self,labelName):
        self.labelName = labelName
            
    def doit(self):
#         '''
#                         这个函数需要改，我只是乱写在这，方便调用
#         @params 
#         @retrun
#         '''
#         from sklearn.pipeline import Pipeline
#         from background_program.b_SampleProcessing.Dimension_Reduction.MyPca import MyPca
#         """=============对训练集进行操作============"""
#         """获取数据"""
#         self.getData()
#         """获取各种器"""
#         preProcesser1, preProcesser2 = self.getPreProcesser()
#         featureSelector, estimater, evalueter = self.getFeatureSelector(), self.getEstimater(), self.getmodelEvalueter()
#        
#         """利用各种器对训练集的特征进行转换"""
#         preProcesser1.fit_transform(self.X_train)
#         preProcesser2.fit_transform(self.X_train)
#         
#         """进行特征选择"""
#         featureSelector.fit(self.X_train, self.Y_train)
#         self.X_train = featureSelector.transform(self.X_train)
#         """利用pca对特征矩阵进行降维"""
#         p = MyPca()
#         n = p.pca_2(self.X_train, 0.99) 
#         self.X_train = p.Train_dataSet(self.X_train, n)
#         """=============对测试集进行操作============"""
#         """利用各种器对测试集的特征进行同训练集一样的转换"""
#         preProcesser1.fit_transform(self.X_test)
#         preProcesser2.fit_transform(self.X_test)
#         self.X_test = featureSelector.transform(self.X_test)
#         
#         """利用pca对特征矩阵进行同训练集一样的降维"""
#         self.X_test = p.Test_dataSet(self.X_test)
#         
#         """进行预测"""
#         estimater.fit(self.X_train, self.Y_train)
#         scores = cross_val_score(estimater,self.X_train,self.Y_train,cv =5)
#         print('Scores',scores)
#         print("Score = ", estimater.score(self.X_test, self.Y_test))
#         
#         Y_pred = estimater.predict(self.X_test)
#         
#         for i in range(len(self.Y_test)):
#             print(self.Y_test[i],Y_pred[i])
#         print('Y_test_type = ',type(self.Y_test))
#         np.random.seed(0)
#         y = np.random.randn(10)
#         print('y')
#         print(y)
#         print(type(y))
#         for i in self.Y_test[:,0]:
#             print(i)
#             
 # 获取数据
        self.get_data()
        # 获取数据预处理器
        pre_processer = self.get_pre_processer()
        # 获取特征选择器
        feature_selector = self.get_feature_selector()
        # 获取特征降维器
        dimension_reductor = MyPca(self.X_train).pca
        # 获取分类器
        estimater = self.get_estimater()
        # 获取模型评估器
        evalueter = self.get_model_evalueter()
        # 管道
        pipeline = Pipeline(
            [('pre_processer', pre_processer),
             ('feature_selector', feature_selector),
             ('dimension_reductor', dimension_reductor),
             ('estimater', estimater),
             ]
            )
        
        """=============对训练集进行操作============"""
        pipeline.fit(self.X_train, self.Y_train)
        
        """=============对测试集进行操作============"""
        Y_pred=predict_result = pipeline.predict(self.X_test)
        
        for i in range(len(Y_pred)):
            print(self.Y_test[i],Y_pred[i])
        print('explained_variance_score:',explained_variance_score(self.Y_test,Y_pred))
        print('mean_absolute_error:',mean_absolute_error(self.Y_test, Y_pred))
        print('mean_squared_error:',mean_squared_error(self.Y_test, Y_pred))
        print('mean_squared_log_error:',mean_squared_log_error(self.Y_test[:,0], Y_pred))
        print('median_absolute_error:',median_absolute_error(self.Y_test, Y_pred))
        print('r2_score:',r2_score(self.Y_test,Y_pred))
        
    def get_data(self):
        '''
                获得训练数据和测试数据
        self.X_train=训练数据特征， self.Y_train=训练数据标签
        self.X_test=测试数据特征， self.Y_test=测试数据标签
        @params string student_num:学生学号
        @retrun
        '''
        from sklearn.model_selection import train_test_split
        from background_program.z_Tools.DataCarer import DataCarer
        iris_data, iris_target = DataCarer().createTrainDataSet_scoreForcasting(self.labelName)  
        self.X_train, self.X_test,self.Y_train, self.Y_test = train_test_split(
        iris_data, iris_target, test_size=0.2, random_state=3)

        
    def get_pre_processer(self):
        '''
                        获得特征预处理器
        @params 
        @retrun    sklearn.PreProcessing.xx preProcesser:特征预处理器
        '''
        from background_program.b_SampleProcessing.PreProcessing.MyMinMaxScaler import MyMinMaxScaler
        from background_program.b_SampleProcessing.PreProcessing.MyImputer import MyImputer
        
        pre_processer = FeatureUnion(
            transformer_list=[
                ('MySelectKBset', MyImputer().transformer),
                ('MySelectPercentile', MyMinMaxScaler().transformer) 
                ],
                n_jobs=2)
        
        return pre_processer
        
    def get_feature_selector(self):
        '''
                        获得特征选择器
        @params 
        @retrun    sklearn.某种类  featureSelector:特征选择器
        '''
        from background_program.b_SampleProcessing.FeatureSelection.MySelectKBest import MySelectKBset
        from background_program.b_SampleProcessing.FeatureSelection.MySelectPercentile import MySelectPercentile
        from sklearn.pipeline import FeatureUnion
        
        featureSelector = FeatureUnion(
            transformer_list=[
                ('MySelectKBset', MySelectKBset().selector),
                ('MySelectPercentile', MySelectPercentile().selector) 
                ],
                n_jobs=1)
        
        return MySelectPercentile().selector
        
    def get_estimater(self):
        '''
                        获得预测器，这里是分类器
        @params 
        @retrun    sklearn.某种类  estimater:预测器
        '''
        from background_program.c_Estimating.Regression.GeneralizedLinearModels.RidgeRegression import RidgeRegression
        
        estimater = RidgeRegression().estimater
        
        return estimater
    
    def get_model_evalueter(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass


if __name__ == '__main__':
    t = score_forcasting('score')
    print(t.doit())
