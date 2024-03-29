'''
奖学金预测模块
@author: jack
'''
from background_program.y_Modules.module_interface import my_module


class scholarship_forcasting(my_module):

    def __init__(self):
#         self.get_dataset()
        my_module.__init__(self, label_name='scholarship_amount',usage='classification')

    def get_features_range(self):
        features_range = my_module.get_features_range(
            self, label_name='scholarship_amount', label_range={'没获得': [0, 0], '有获得': [1, 99999], })

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
        from background_program.b_Sample_processing.PreProcessing.MyImputer import MyImputer

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
        from background_program.b_Sample_processing.Feature_selection.MySelectKBest import MySelectKBset

        featureSelector = MySelectKBset().selector

        return featureSelector

    def get_estimater(self):
        '''
        获得预测器，这里是分类器
        @params
        @retrun    sklearn.某种类  estimater:预测器
        '''
        from background_program.c_Estimating.Classification import My_Cart

        estimater = My_Cart().estimater

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
    t = scholarship_forcasting()
