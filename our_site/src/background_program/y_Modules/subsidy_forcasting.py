'''
Created on 2017年12月17日

@author: jack
'''
from background_program.y_Modules.module_interface import my_module


class subsidy_forcasting(my_module):
    
    def __init__(self):
        my_module.__init__(self, label_name='subsidy_amount')
            
    def get_dataset(self):
        my_module.get_dataset(self, school_year='2016', usage='regression')
        
    def get_features_range(self):
        features_range = my_module.get_features_range(self, label_name='subsidy_amount', label_range={'A':[0, 60], 'B':[60, 90], 'C':[90, 100]})
        
        return features_range
         
    def get_pre_processer(self):
        '''
                        获得特征预处理器
        @params 
        @retrun    sklearn.PreProcessing.xx preProcesser:特征预处理器
        '''
        from sklearn.pipeline import FeatureUnion
        from background_program.b_SampleProcessing.PreProcessing.MyImputer import MyImputer
        
        pre_processer = FeatureUnion(
            transformer_list=[
                ('MySelectKBset', MyImputer().transformer),
                ],
                n_jobs=2)
        
        return pre_processer
        
    def get_feature_selector(self):
        '''
                        获得特征选择器
        @params 
        @retrun    sklearn.某种类  featureSelector:特征选择器
        '''
        from sklearn.pipeline import FeatureUnion
        from background_program.b_SampleProcessing.FeatureSelection.MySelectKBest import MySelectKBset
        from background_program.b_SampleProcessing.FeatureSelection.MySelectPercentile import MySelectPercentile
        
        featureSelector = FeatureUnion(
            transformer_list=[
                ('MySelectKBset', MySelectKBset().selector),
                ('MySelectPercentile', MySelectPercentile().selector) 
                ],
                n_jobs=1)
        
        return featureSelector
        
    def get_estimater(self):
        '''
                        获得预测器，这里是分类器
        @params 
        @retrun    sklearn.某种类  estimater:预测器
        '''
        from background_program.c_Estimating.Classification.Tree.MyDecesionTree import MyDecesionTree
        
        estimater = MyDecesionTree().estimater
        
        return estimater
    
    def get_model_evalueter(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass


if __name__ == '__main__':
    t = subsidy_forcasting()
    print(t.predict())
