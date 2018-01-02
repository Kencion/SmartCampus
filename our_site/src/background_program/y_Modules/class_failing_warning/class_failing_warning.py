'''
挂科预警模块
Created on 2017年7月22日
Modify on 2017年11月27日
@author: jack
'''
from sklearn.pipeline import FeatureUnion


class class_failing_warning():
    
    def __init__(self):
        self.label_name = 'score'
        # 获取数据
        self.get_data()
        # 获取数据预处理器
        self.pre_processer = self.get_pre_processer()
        # 获取特征选择器
        self.feature_selector = self.get_feature_selector()
        # 获取分类器
        self.estimater = self.get_estimater()
        # 获取模型评估器
        self.evalueter = self.get_model_evalueter()
            
    def predict(self):
        '''
                        这个函数需要改，我只是乱写在这，方便调用
        @params 
        @retrun
        '''
        from sklearn.pipeline import Pipeline
        
        pipeline = Pipeline(
            [('pre_processer', self.pre_processer),
             ('feature_selector', self.feature_selector),
             ('estimater', self.estimater),
             ]
            )
        
        pipeline.fit(self.X_train, self.Y_train)
        predict_result = pipeline.predict(self.X_test)
        
        result = []
        for student, score in zip(self.students, predict_result):
            result.append([student.getStudent_num(), score])
            
        return result
    
    def get_features_range(self):
        pass
    
    def get_data(self):
        '''
                        获得训练数据和测试数据
        self.X_train=训练数据特征， self.Y_train=训练数据标签
        self.X_test=测试数据特征， self.Y_test=测试数据标签
        @params string student_num:学生学号
        @retrun
        '''
        from background_program.a_Data_prossing.DataCarer import DataCarer
        
        data_carer = DataCarer(label_name=self.label_name, school_year='2016', usage="classify")
        self.X_train, self.Y_train = data_carer.create_train_dataSet()  
        self.students, self.X_test = data_carer.create_validate_dataSet()
        
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
    
    def get_model_evalueter(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass


if __name__ == '__main__':
    t = class_failing_warning()
    print(t.predict())
