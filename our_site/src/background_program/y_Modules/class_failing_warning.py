'''
挂科预警模块
Created on 2017年7月22日
Modify on 2017年11月27日
@author: jack
'''
from sklearn.pipeline import FeatureUnion
from background_program.y_Modules.module_interface import my_module


class class_failing_warning(my_module):
    
    def __init__(self):
        my_module.__init__(self, label_name='score')
            
    def get_features_range(self):
        pass
    
    def get_dataset(self):
        my_module.get_dataset(self, school_year='2016', usage='classify')
        
    def get_pre_processer(self):
        '''
                        获得特征预处理器
        @params 
        @retrun    sklearn.PreProcessing.xx preProcesser:特征预处理器
        '''
        from background_program.b_Sample_processing.PreProcessing.MyMinMaxScaler import MyMinMaxScaler
        from background_program.b_Sample_processing.PreProcessing.MyImputer import MyImputer
        
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
        from background_program.b_Sample_processing.Feature_selection.MySelectKBest import MySelectKBset
        from background_program.b_Sample_processing.Feature_selection.MySelectPercentile import MySelectPercentile
        
#         feature_selector = FeatureUnion(
#             transformer_list=[
#                 ('MySelectKBset', MySelectKBset().selector),
#                 ('MySelectPercentile', MySelectPercentile().selector) 
#                 ],
#                 n_jobs=2)
#          
#         return feature_selector
        return MySelectKBset().selector
        
    def get_estimater(self):
        '''
                        获得预测器，这里是分类器
        @params 
        @retrun    sklearn.某种类  estimater:预测器
        '''
        from background_program.c_Estimating.Classification.Tree.MyDecesionTree import MyDecesionTree
        
        estimater = MyDecesionTree().estimater
        return estimater
    
    def get_model_evaluater(self, y_true, y_predict):
        '''
                        获得模型评估器，这里用roc曲线下的面积，即auc来评价
        @params 
        @retrun    
        '''
        from background_program.d_Model_evaluating.Regression import my_explained_variance_score
        
        model_evalueter = my_explained_variance_score(y_true, y_predict)
        
        return model_evalueter


if __name__ == '__main__':
    t = class_failing_warning()
    print(t.predict())
