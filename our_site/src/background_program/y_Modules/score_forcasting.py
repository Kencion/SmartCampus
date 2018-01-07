'''
@author: LI Created on 2017年12月17日
@modify: Jack Modify on 2018年1月3日
'''
from background_program.y_Modules.module_interface import my_module


class score_forcasting(my_module):
    
    def __init__(self):
        my_module.__init__(self, label_name='score')
            
    def get_features_range(self):
        features_range = my_module.get_features_range(self, label_name='score', label_range={'A':[0, 60], 'B':[60, 90], 'C':[90, 100]})
        
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
        from background_program.b_SampleProcessing.PreProcessing.MyMinMaxScaler import MyMinMaxScaler
        from background_program.b_SampleProcessing.PreProcessing.MyImputer import MyImputer
        
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
        from background_program.b_SampleProcessing.FeatureSelection.MySelectKBest import MySelectKBset
        from background_program.b_SampleProcessing.FeatureSelection.MySelectPercentile import MySelectPercentile
        
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
    
    def get_model_evalueter(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass
    
    def hhh(self):
        '''
                        数据的转换，转成echarts能识别的格式
        @return: data,json格式
        '''
        import operator
        
        info = self.get_features_range()
#         print(info)
        data = {}
        name = 'name'
        children = 'children'
        list2 = []
        #获得当前类名
        data[name] = self.__class__.__name__
        #获得特征的评分
        d = self.get_feature_scores()
        #对特征按照评分进行排序
        d = sorted(d.items(),key = operator.itemgetter(1))
        #取评分前十个存储
        for d_index in range(len(d)-10,len(d)):
            list1 = []
            dic2 = {}
            dic2[name] = d[d_index][0]
            
            for i in info[d[d_index][0]]:
                dic1 = {}
                dic1[name] = str(i) + ":" + str(info[d[d_index][0]][i])
                list1.append(dic1)
                
            dic2[children] = list1
            list2.append(dic2)
            
        data[children] = list2
        
        return data


if __name__ == '__main__':
    t = score_forcasting()


