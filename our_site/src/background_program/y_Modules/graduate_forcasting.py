'''
Forcasting weather a student can graduate or not

Created on 2018年4月20日

@author: Jack
'''
from background_program.y_Modules.module_interface import my_module


class graduate_forcasting(my_module):

    def __init__(self):
        my_module.__init__(self, label_name='graduate')

    def get_features_range(self):
        features_range = my_module.get_features_range(self, label_name='graduate', label_range={'可以毕业': [0, 1], '不可以毕业': [1, 2]})

        return features_range

    def get_dataset(self):
        my_module.get_dataset(self, school_year='2016', usage='classification')

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
        from background_program.d_Model_evalueting.Classification import accuracy_score

        model_evalueter = accuracy_score(y_true, y_predict)

        return model_evalueter


if __name__ == '__main__':
    t, tt = graduate_forcasting().predict()
    for i in tt:
        print(i)
