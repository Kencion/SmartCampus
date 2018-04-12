'''
@modify: Jack Modify on 2018年1月3日
'''
import numpy as np
from sklearn.model_selection import train_test_split


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
        
        self.evaluate_score = 0
            
    def predict(self):
        from sklearn.pipeline import Pipeline
        
        # 管道
#         pipeline = Pipeline(
#             [('pre_processer', self.pre_processer),
#              ('feature_selector', self.feature_selector),
#              ('estimater', self.estimater),
#              ]
#             )
        pipeline = Pipeline(
            [('pre_processer', self.pre_processer),
             ('estimater', self.estimater),
             ]
            )
        
        pipeline.fit(self.X_train, self.Y_train) 
        predict_result = pipeline.predict(self.X_test)
         
        result = []
        for student, score in zip(self.students, predict_result):
            result.append([student.getStudent_num(), float(score)])
        
        # evaluete_score
        predict_result = pipeline.predict(self.X_validate)
        evaluete_score = self.get_evaluate_score(y_true=[i[0] for i in self.Y_validate.tolist()],
                                                    y_predict=[i for i in predict_result])
        self.evaluate_score = evaluete_score
        return evaluete_score, result
        
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
        from .feature_name import features_name_ch
        for i in range(len(f_scores)):
            feature_scores[features_name_ch[i].strip()] = f_scores[i] 
        
        return feature_scores   
    
    def get_features_range(self, label_name, label_range):
        '''
                        获得每个特征的范围
        @params 
        @retrun 问龙天
        '''
        from background_program.a_Data_prossing.DataCarer import DataCarer
        
        data_carer = DataCarer(label_name=self.label_name, school_year='2016', usage="regression")

        from .feature_name import features_name_ch, features_name_en

        fs_name, fs_name_ch = [], []
        for f_name, f_name_ch in zip(features_name_en, features_name_ch):
            fs_name.append(f_name.strip())
            fs_name_ch.append(f_name_ch.strip())
        
        features_range = dict()
        for f_name, f_name_ch in zip(fs_name, fs_name_ch):
            rangee = dict()
            for score_type, score_range in zip(label_range.keys(), label_range.values()):
                rangee[score_type] = data_carer.get_feature_range(
                                                f_name, label_name=label_name,
                                                label_min=score_range[0], label_max=score_range[1])

            features_range[f_name_ch] = rangee
        
        return features_range
         
    def get_dataset(self, school_year='2016', usage='regression'):
        '''
                获得训练数据和测试数据
        self.X_train=训练数据特征， self.Y_train=训练数据标签
        self.X_test=测试数据特征
        @params string student_num:学生学号
        @retrun
        '''
        from background_program.a_Data_prossing.DataCarer import DataCarer
        
        data_carer = DataCarer(label_name=self.label_name, school_year=school_year, usage=usage)
        
        X_train, Y_train = data_carer.create_train_dataSet()
         
        self.X_train, self.X_validate, self.Y_train, self.Y_validate = train_test_split(
        X_train, Y_train, test_size=0.2, random_state=3)
        
        self.X_train = np.array(self.X_train)
        self.X_validate = np.array(self.X_validate)
        self.Y_train = np.array(self.Y_train)
        self.Y_validate = np.array(self.Y_validate)
        
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
    
    def get_model_evaluater(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass
    
    def get_tree_data(self):
        '''
                        数据的转换，转成echarts树形图能识别的格式
        @return: data,json格式
        '''
        import operator

        info = self.get_features_range()
        data = {}
        name = 'name'
        children = 'children'
        value = 'value'
        list2 = []
        # 获得当前类名
        data[name] = ''
        # 获得特征的评分
        d = self.get_feature_scores()
        # 对特征按照评分进行排序
        d = sorted(d.items(), key=operator.itemgetter(1))
        # 取评分前十个存储
        for d_index in range(len(d) - 10, len(d)):
            list1 = []
            dic2 = {}
            dic2[name] = d[d_index][0]
            if d[d_index][1] == float("inf"):
                dic2[value] = 9999
            else:
                dic2[value] = float(d[d_index][1]) 
            for i in info[d[d_index][0]]:
                dic1 = {}
                dic1[name] = str(i) + ":" + str(info[d[d_index][0]][i])
                list1.append(dic1)
                
            dic2[children] = list1
            list2.append(dic2)
            
        data[children] = list2
        
        return data
