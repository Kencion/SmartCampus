'''
@author: LI Created on 2017年12月17日
@modify: Jack Modify on 2018年1月3日
'''
from background_program.y_Modules.module_interface import my_module


class score_forcasting(my_module):

    def __init__(self):
        my_module.__init__(self, label_name='score')

    def get_features_range(self):
        features_range = my_module.get_features_range(self, label_name='score', label_range={
                                                      '不及格': [0, 60], '60分-90分': [60, 90], '90分以上': [90, 100]})

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

    def get_model_evaluater(self, y_true, y_predict):
        '''
                        获得模型评估器，这里用roc曲线下的面积，即auc来评价
        @params 
        @retrun    
        '''
        from background_program.d_Model_evalueting.Regression import adjusted_mutual_info_score

        model_evalueter = adjusted_mutual_info_score(y_true, y_predict)

        return model_evalueter


    
if __name__ == '__main__':
    t, tt = score_forcasting().predict()
    print(t)
    print(tt)

