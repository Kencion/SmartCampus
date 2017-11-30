'''
Created on 2017年7月22日
Modify on 2017年11月27日
算法融合

@author: jack
'''

class ClassFailingWarning():
    
    def __init__(self):
        from sklearn.pipeline import Pipeline
        
        self.getData()
        preProcesser1, preProcesser2 = self.getPreProcesser()
        featureSelector, estimater, evalueter = self.getFeatureSelector(), self.getEstimater(), self.getmodelEvalueter()
        hahaha = Pipeline(
            [   ('preProcesser1', preProcesser1),
                ('preProcesser2', preProcesser2),
                ('featureSelector', featureSelector),
                ('estimater', estimater)                ]
            )
        hahaha.fit(self.X_train, self.Y_train)
        print("准确率", hahaha.score(self.X_train, self.Y_train))
        for student, score in zip(self.students, hahaha.predict(self.X_test)):
            print(student.getStudent_num(), "----", score)
            
    
    def getData(self):
        """
         get train data and test data
        """
        from z_Tools import DataCarer
        self.X_train, self.Y_train = DataCarer.createTrainDataSet()  
        self.students, self.X_test = DataCarer.createValidateDataSet()
        
    def getPreProcesser(self):
        '''
        获得特征预处理器
        '''
        from b_SampleProcessing.PreProcessing.MyMinMaxScaler import MyMinMaxScaler
        from b_SampleProcessing.PreProcessing.MyImputer import MyImputer
        
        return MyImputer().transformer, MyMinMaxScaler().transformer
        
    def getFeatureSelector(self):
        '''
        获得特征选择器
        '''
        from b_SampleProcessing.FeatureSelection.MySelectKBest import MySelectKBset
        from b_SampleProcessing.FeatureSelection.MySelectPercentile import MySelectPercentile
        from sklearn.pipeline import FeatureUnion
        
        return FeatureUnion(
            transformer_list=[
                ('MySelectKBset', MySelectKBset().selector),
                ('MySelectPercentile', MySelectPercentile().selector) 
                ],
                n_jobs=2)
        
    def getEstimater(self):
        '''
        获得预测器，这里是分类器
        '''
        from c_Estimating.Classification.Tree.MyDecesionTree import MyDecesionTree
        
        return MyDecesionTree().estimater
    
    def getmodelEvalueter(self):
        '''
        获得模型评估器，主要是评估算法正确率
        '''
        pass


if __name__ == '__main__':
    t = ClassFailingWarning()
