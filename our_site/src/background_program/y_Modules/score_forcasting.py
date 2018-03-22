'''
@author: LI Created on 2017年12月17日
@modify: Jack Modify on 2018年1月3日
'''
from background_program.y_Modules.module_interface import my_module


class score_forcasting(my_module):
    
    def __init__(self):
        my_module.__init__(self, label_name='score')
            
    def get_features_range(self):
        features_range = my_module.get_features_range(self, label_name='score', label_range={'不及格':[0, 60], '60分-90分':[60, 90], '90分以上':[90, 100]})
        
        return features_range
         
    def get_dataset(self):
        my_module.get_dataset(self, school_year='2016', usage='regression')
        
    def get_pre_processer(self):
        '''
                        获得特征预处理器
        @params 
        @retrun    sklearn.PreProcessing.xx preProcesser:特征预处理器
        '''
        from sklearn.pipeline import FeatureUnion
        from background_program.b_Sample_processing.PreProcessing.MyMinMaxScaler import MyMinMaxScaler
        from background_program.b_Sample_processing.PreProcessing.MyImputer import MyImputer
        
        pre_processer = FeatureUnion(
            transformer_list=[
                ('MyImputer', MyImputer().transformer),
                ('MyMinMaxScaler', MyMinMaxScaler().transformer) 
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
        from background_program.b_Sample_processing.Feature_selection.MySelectKBest import MySelectKBset
        from background_program.b_Sample_processing.Feature_selection.MySelectPercentile import MySelectPercentile
        
#         featureSelector = FeatureUnion(
#             transformer_list=[
#                 ('MySelectKBset', MySelectKBset().selector),
#                 ('MySelectPercentile', MySelectPercentile().selector) 
#                 ],
#                 n_jobs=1)
#          
#         return featureSelector
        return MySelectKBset().selector
        
    def get_estimater(self):
        '''
                        获得预测器，这里是分类器
        @params 
        @retrun    sklearn.xx estimater:预测器
        '''
        from background_program.c_Estimating.Regression.GeneralizedLinearModels.RidgeRegression import RidgeRegression
        
        estimater = RidgeRegression().estimater
        
        return estimater
    
    def get_model_evalueter(self, y_true, y_predict):
        '''
                        获得模型评估器，这里用roc曲线下的面积，即auc来评价
        @params 
        @retrun    
        '''
        from sklearn.metrics import roc_auc_score
        import numpy as np
        
        print(y_true)
        print(y_predict)
        
        model_evalueter = roc_auc_score(np.array(y_true), np.array(y_predict))
        print(1)
        
        return model_evalueter

    def get_pie_data(self):
        '''
                        获得echarts画饼图需要的数据
        @params 
        @retrun data list类型数据
        '''
        info = self.predict()[1]
        score_list = [x[1] for x in info]

        score = {'60分以下':0, '60分-70分':0, '70分-80分':0, '80分-90分':0, '90分及以上':0}
        
        for index in score_list:
            if index < 60:
                score['60分以下'] += 1
            if index < 70 and index >= 60:
                score['60分-70分'] += 1
            if index < 80 and index >= 70:
                score['70分-80分'] += 1
            if index < 90 and index >= 80:
                score['80分-90分'] += 1
            if index <= 100 and index >= 90:
                score['90分-100分'] += 1
 
        data = []
        for name in score:
            dic = {}
            dic['name'] = name
            dic['value'] = score[name]
            data.append(dic)
        return data   


if __name__ == '__main__':
    tt, t = score_forcasting().predict()
    print(tt)
