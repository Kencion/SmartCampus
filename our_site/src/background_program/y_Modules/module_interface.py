'''
@modify: Jack Modify on 2018年1月3日
'''
import math
from numpy import mat
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.externals import joblib


class my_module():

    def __init__(self, label_name):
        self.labellist = []
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

        self.predict_result = None
        
    def train_model(self, train_time):
        from sklearn.pipeline import Pipeline

        # 管道
        pipeline = Pipeline(
            [('pre_processer', self.pre_processer),
             ('feature_selector', self.feature_selector),
             ('estimater', self.estimater),
             ]
        )
        
        for _ in range(train_time):
            pipeline.fit(self.X_train, self.Y_train)
            
        self.estimater = pipeline

    def predict(self):
        self.train_model(train_time=10)
        
        # evaluete_score
        predict_result = self.estimater.predict(self.X_validate)
        model_evalueter = self.get_model_evaluater(y_true=[i[0] for i in self.Y_validate.tolist()],
                                                   y_predict=[i for i in predict_result])
        self.evaluete_score = model_evalueter.get_evaluate_score()

        # get predict result
        predict_result = self.estimater.predict(self.X_test)
        result = []
        for student, score in zip(self.students, predict_result):
            result.append([student.getStudent_num(), float(score)])

        self.predict_result = result

        return self.evaluete_score, result

    def get_evaluate_score(self):
        '''
        @return: evaluate_score
        '''

        return self.evaluate_score

    def get_feature_scores(self):
        '''
                        获得每个特征得到的评分
        @params 
        @retrun    dict selected_features:每个特征的评分
        '''
        import operator
        from .feature_name import features_name_ch
        
        # 获取特征选择器
        feature_selector = self.get_feature_selector()

        feature_selector.fit(self.X_train, self.Y_train)
        f_scores = feature_selector.scores_
        
        feature_scores = dict()
        for i in range(len(f_scores)):
            if math.isinf(f_scores[i]):
                feature_scores[features_name_ch[i].strip()] = 999999
            elif math.isnan(f_scores[i]):
                pass
            else:
                feature_scores[features_name_ch[i].strip()] = f_scores[i]
        feature_scores = sorted(
            feature_scores.items(), key=operator.itemgetter(1))

        return feature_scores

    def get_features_range(self, label_name, label_range):
        '''
                        获得每个特征的范围
        @params 
        @retrun 每个特征的范围
        '''
        from background_program.a_Data_prossing.DataCarer import DataCarer

        data_carer = DataCarer(label_name=self.label_name,
                               school_year='2016', usage="regression")

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

        data_carer = DataCarer(label_name=self.label_name,
                               school_year=school_year, usage=usage)
        self.labellist = data_carer.labellist.copy()

        X_train, Y_train = data_carer.create_train_dataSet()
        self.X_train, self.X_validate, self.Y_train, self.Y_validate = train_test_split(
            X_train, Y_train, test_size=0.8, random_state=5)

        self.X_train = mat(self.X_train, dtype=float)
        self.X_validate = mat(self.X_validate, dtype=float)
        self.Y_train = mat(self.Y_train, dtype=float)
        self.Y_validate = mat(self.Y_validate, dtype=float)

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

    def predict2(self):
        from sklearn.pipeline import Pipeline

        # 管道
        pipeline = Pipeline(
            [('pre_processer', self.pre_processer),
             ('feature_selector', self.feature_selector),
             ('estimater', self.estimater),
             ]
        )

        pipeline.fit(self.X_train, self.Y_train)
        ree = pipeline.named_steps['feature_selector'].get_support()
        predict_result = pipeline.predict(self.X_test)

        result = np.array(predict_result.copy())
#         for student, score in zip(self.students, predict_result):
#             result.append([student.getStudent_num(), float(score)])

        # evaluete_score
        predict_result = pipeline.predict(self.X_validate)
        self.evaluete_score = self.get_model_evaluater(y_true=[i[0] for i in self.Y_validate.tolist()],
                                                    y_predict=[i for i in predict_result]).get_evaluate_score()

        return self.evaluete_score, result

    def persistence_model(self):
        '''
        将模型持久化
        '''
        joblib.dump(self.estimater, 'train_model')

    def load_model(self):
        '''
        从文件中加载模型
        '''
        self.estimater = joblib('train_model')
        
    def predictbyLi(self):
        from sklearn.pipeline import Pipeline

        # 管道
        pipeline = Pipeline(
            [('pre_processer', self.pre_processer),
             ('feature_selector', self.feature_selector),
             ('estimater', self.estimater),
             ]
        )

        pipeline.fit(self.X_train, self.Y_train)
        ree = pipeline.named_steps['feature_selector'].get_support()
        for i in range(len(ree)):
            if ree[i] == True:
                print(self.labellist[i])
        predict_result = pipeline.predict(self.X_test)

        result = np.array(predict_result.copy())

        predict_result = pipeline.predict(self.X_validate)
        y_true = [i[0] for i in self.Y_validate.tolist()]
        y_predict = [i for i in predict_result]

        return y_true, y_predict, result
