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
        featureSelector, estimater, evalueter = self.getFeatureSelector(), self.getEstimater(), self.getmodelEvalueting()
        hahaha = Pipeline(
            [('featureSelector', featureSelector),
              ('estimater', estimater)
                ]
            )
        hahaha.fit(self.X_train, self.Y_train)
        print(hahaha.score(self.X_train, self.Y_train))
    
    def getData(self):
        """
         get train data and test data
        """
        from z_Tools import DataCarer
        self.X_train, self.Y_train = DataCarer.createTrainDataSet()  
        self.students, self.X_test = DataCarer.createValidateDataSet()
        
    def getFeatureSelector(self):
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
        from c_Estimating.Classification.Tree.MyDecesionTree import MyDecesionTree
        return MyDecesionTree().clf
    
    def getmodelEvalueting(self):
        pass


if __name__ == '__main__':
    t = ClassFailingWarning()
