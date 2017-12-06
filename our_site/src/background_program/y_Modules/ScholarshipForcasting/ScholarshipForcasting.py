'''
奖学金预测模块
Created on 2017年7月22日
Modify on 2017年11月27日
@author: jack
'''

class ScholarshipForcasting():
    
    def __init__(self):
        from sklearn.pipeline import Pipeline
        from b_SampleProcessing.Dimension_Reduction.Pca_Test import Pca_Test
        
        """=============对训练集进行操作============"""
        """获取数据"""
        self.getData()
        
        """获取各种器"""
        preProcesser1, preProcesser2 = self.getPreProcesser()
        featureSelector, estimater, evalueter = self.getFeatureSelector(), self.getEstimater(), self.getmodelEvalueter()
       
        """利用各种器对训练集的特征进行转换"""
        preProcesser1.fit_transform(self.X_train)
        preProcesser2.fit_transform(self.X_train)
        
        """进行特征选择"""
        featureSelector.fit_transform(self.X_train, self.Y_train)
        
        """利用pca对特征矩阵进行降维"""
        p = Pca_Test()
        n = p.pca_2(self.X_train, 0.99) 
        p.Train_dataSet(self.X_train, n)
        
        """=============对测试集进行操作============"""
        """利用各种器对测试集的特征进行同训练集一样的转换"""
        preProcesser1.fit_transform(self.X_test)
        preProcesser2.fit_transform(self.X_test)
        
        """利用pca对特征矩阵进行同训练集一样的降维"""
        p.Test_dataSet(self.X_test)
        
        """进行预测"""
        estimater.fit(self.X_train, self.Y_train)
        print("准确率", estimater.score(self.X_train, self.Y_train))
        
        for student, score in zip(self.students, estimater.predict(self.X_test)):
            if score != 0.0:
                print(student.getStudent_num(), "----", score)
            
    
    def getData(self):
        '''
                        获得训练数据和测试数据
        self.X_train=训练数据特征， self.Y_train=训练数据标签
        self.X_test=测试数据特征， self.Y_test=测试数据标签
        @params string student_num:学生学号
        @retrun
        '''
        from z_Tools.DataCarer import DataCarer
        self.X_train, self.Y_train = DataCarer().createTrainDataSet()  
        self.students, self.X_test = DataCarer().createValidateDataSet()
        
    def getPreProcesser(self):
        '''
                        获得特征预处理器
        @params 
        @retrun    sklearn.PreProcessing.xx preProcesser:特征预处理器
        '''
        from b_SampleProcessing.PreProcessing.MyMinMaxScaler import MyMinMaxScaler
        from b_SampleProcessing.PreProcessing.MyImputer import MyImputer
        
        preProcesser = MyImputer().transformer, MyMinMaxScaler().transformer
        
        return preProcesser
        
    def getFeatureSelector(self):
        '''
                        获得特征选择器
        @params 
        @retrun    sklearn.某种类  featureSelector:特征选择器
        '''
        from b_SampleProcessing.FeatureSelection.MySelectKBest import MySelectKBset
        from b_SampleProcessing.FeatureSelection.MySelectPercentile import MySelectPercentile
        from sklearn.pipeline import FeatureUnion
        
        featureSelector = FeatureUnion(
            transformer_list=[
                ('MySelectKBset', MySelectKBset().selector),
                ('MySelectPercentile', MySelectPercentile().selector) 
                ],
                n_jobs=1)
        
        return featureSelector
        
    def getEstimater(self):
        '''
                        获得预测器，这里是分类器
        @params 
        @retrun    sklearn.某种类  estimater:预测器
        '''
        from c_Estimating.Classification.Tree.MyDecesionTree import MyDecesionTree
        
        estimater = MyDecesionTree().estimater
        
        return estimater
    
    def getmodelEvalueter(self):
        '''
                        获得模型评估器，主要是评估算法正确率
        @params 
        @retrun    
        '''
        pass


if __name__ == '__main__':
    t = ClassFailingWarning()