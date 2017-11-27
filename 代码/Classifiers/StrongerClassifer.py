'''
Created on 2017年7月22日
Modify on 2017年11月27日
算法融合

@author: jack
'''
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.externals import joblib
from numpy import mat
from Tools import DataCarer
from SingleClassifiers import *

class StrongerClassifer():
    
    def __init__(self):
        # weak classifiers
        self.clfs = [
            DecesionTree.DecesionTree().getBestOne('DecesionTree'),
#             ExtraTrees.ExtraTrees().getBestOne('ExtraTrees'),
#             GaussianNB.GaussianNB().getBestOne('GaussianNB'),
#             GaussianProcesses.GaussianProcesses().getBestOne('GaussianProcesses'),
#             MLP.MLP().getBestOne('MLP'),
#             NearestNeighbors.NearestNeighbors().getBstOne('NearestNeighbors'),
#             RandomForest.RandomForest().getBestOne('RandomForest'),
#             SGD.SGD().getBestOne('SGD'),
#             SVC.SVC().getBestOne('SVC'),
            ]
        # final classifier
        self.finalClassifier = VotingClassifier(estimators=[
                ('0', self.clfs[0]),
                ],
               voting='soft',
               weights=[1, ])

    def getData(self):
        # get train data and test data
        self.X_train, self.Y_train = DataCarer.createTrainDataSet()  
        self.students, self.X_test = DataCarer.createValidateDataSet()

    def haha(self):
        self.getData()
        # 特征选择
        self.clfs[0].fit(self.X_train, self. Y_train)
        self.fetureSelecter = SelectFromModel(DecesionTree)
#         self.fetureSelecter = SelectFromModel(self.clfs[0], prefit=True)
#         
#         print(self.fetureSelecter._get_support_mask())
#         print(self.fetureSelecter.get_support(indices=True))  # display importance of each variables
        
        clf = Pipeline([
#         ('fetureSelection', self.fetureSelecter),
        ('classification', self.finalClassifier)
        ])
        
        # save the classifier as a dump
        X, Y = DataCarer.createTrainDataSet()
        accuracyRates = []
        for i in range(1, 2):
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
            clf.fit(X_train, Y_train)
            for i, j in zip(X_test.tolist(), clf.predict(X_test).tolist()):
                print(j)
                print("---")
                print(i)
            accuracyRates.append(clf.score(X_test, Y_test))
            if i == 1:
                joblib.dump(clf, 'final.pkl')
                
        # 输出正确率的均值
        print(mat(accuracyRates).mean())

if __name__ == '__main__':
    t = StrongerClassifer()
    t.haha()
