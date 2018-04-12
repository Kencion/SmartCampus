'''
奖学金预测模块
@author: jack Created on 2017年12月19日
'''
from background_program.y_Modules.module_interface import my_module


class scholarship_forcasting(my_module):
    
    def __init__(self):
        my_module.__init__(self, label_name='scholarship_amount')
            
    def get_features_range(self):
        '''
        @retrun    特征范围
        '''
        features_range = my_module.get_features_range(self, label_name='scholarship_amount', label_range={'没获得':[0, 0], '有获得':[1, 99999], })
        
        return features_range
    
    def get_data(self):
        '''
        get train,test,validation dataSet
        '''
        my_module.get_dataset(self, school_year='2016', usage='regression')
        
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
        from background_program.c_Estimating.Regression.GeneralizedLinearModels.RidgeRegression import RidgeRegression
        
        estimater = RidgeRegression().estimater
        
        return estimater
    
    def get_evaluate_score(self, y_true, y_predict):
        '''
                        获得模型评估器，这里用roc曲线下的面积，即auc来评价
        @params 
        @retrun    
        '''
        from background_program.d_Model_evaluating.Regression import my_explained_variance_score
        
        evaluate_score = my_explained_variance_score(y_true, y_predict)
        
        return evaluate_score
    
    def get_pie_data(self):
        '''
                        获得echarts画饼图需要的数据
        @params 
        @retrun data list类型数据
        '''
        info = self.predict()[1]
        
        #获得奖学金获奖名单
        scholarship_list = [x[1] for x in info]
        scholarship = {'获得奖学金':0,'未获得奖学金':0}
        
        #统计获得和未获得奖学金的人数
        for index in scholarship_list:
            if index > 0 :
                scholarship['获得奖学金'] += 1
            if index <= 0:
                scholarship['未获得奖学金'] += 1
        
        data = []
        for name in scholarship:
            dic = {}
            dic['name'] = name
            dic['value'] = scholarship[name]
            data.append(dic)

        return data   
    
    

if __name__ == '__main__':
    pass
#     t = scholarship_forcasting()
