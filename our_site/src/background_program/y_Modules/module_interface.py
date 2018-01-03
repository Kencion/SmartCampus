'''
@modify: Jack Modify on 2018年1月3日
'''


class my_module():
    
    def __init__(self, label_name):
        self.label_name = label_name
        # 获取数据
        self.get_dataset()
        # 获取数据预处理器
        self.pre_processer = self.get_pre_processer()
        # 获取特征选择器
        self.feature_selector = self.get_feature_selector()
        # 获取分类器
        self.estimater = self.get_estimater()
        # 获取模型评估器
        self.evalueter = self.get_model_evalueter()
            
    def predict(self):
        from sklearn.pipeline import Pipeline
        
        # 管道
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
            result.append([student.getStudent_num(), float(score)])
        
        return 2, result
        
    def get_feature_scores(self):
        '''
                        获得每个特征得到的评分
        @params 
        @retrun    dict selected_features:每个特征的评分
        '''
        # 获取特征选择器
        feature_selector = self.get_feature_selector()
        
        feature_selector.fit(self.X_train, self.Y_train)
        feature_scores = dict()
        f_scores = feature_selector.scores_
        with open('feature_name', 'r') as f:
            feature_names = f.readlines()
            for i in range(len(f_scores)):
                feature_scores[feature_names[i].strip()] = f_scores[i] 
        
        return feature_scores   
    
    def get_features_range(self, label_name, label_range):
        '''
                        获得每个特征的范围
        @params 
        @retrun 问龙天
        '''
        from background_program.a_Data_prossing.DataCarer import DataCarer
        
        data_carer = DataCarer(label_name=self.label_name, school_year='2016', usage="regression")
        features_name = []
        with open('feature_name', 'r') as f:
            for feature_name in f.readlines():
                features_name.append(feature_name.strip())
        
        features_range = dict()
        for feature_name in features_name:
            rangee = dict()
            for score_type, score_range in zip(label_range.keys(), label_range.values()):
                rangee[score_type] = data_carer.get_feature_range(
                                                feature_name, label_name=label_name,
                                                label_min=score_range[0], label_max=score_range[1])

            features_range[feature_name] = rangee
        
        return features_range
         
    def get_dataset(self, school_year='2016', usage='regression'):
        '''
                获得训练数据和测试数据
        self.X_train=训练数据特征， self.Y_train=训练数据标签
        self.X_test=测试数据特征， self.Y_test=测试数据标签
        @params string student_num:学生学号
        @retrun
        '''
        from background_program.a_Data_prossing.DataCarer import DataCarer
        
        data_carer = DataCarer(label_name=self.label_name, school_year=school_year, usage=usage)
        self.X_train, self.Y_train = data_carer.create_train_dataSet() 
        self.students, self.X_test = data_carer.create_validate_dataSet()
        
    def get_pre_processer(self):
        '''
                        获得特征预处理器
        @params 
        @retrun    sklearn.PreProcessing.xx preProcesser:特征预处理器
        '''
        pass
        
    def get_feature_selector(self):
        
        '''
                        获得特征选择器
        @params 
        @retrun    sklearn.某种类  featureSelector:特征选择器
        '''
        pass
        
    def get_estimater(self):
        '''
                        获得预测器，这里是分类器
        @params 
        @retrun    sklearn.xx estimater:预测器
        '''
        pass
    
    def get_model_evalueter(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass
