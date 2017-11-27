'''
算法融合
'''
from Tools import DataCarer
from sklearn.pipeline import Pipeline
from numpy import mat
from sklearn.feature_selection import SelectFromModel, SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from SingleClassifiers import *
from sklearn.externals import joblib

# single classifier
DecesionTree = DecesionTree.DecesionTree().getBestOne('DecesionTree')
ExtraTrees = ExtraTrees.ExtraTrees().getBestOne('ExtraTrees')
GaussianNB = GaussianNB.GaussianNB().getBestOne('GaussianNB')
GaussianProcesses = GaussianProcesses.GaussianProcesses().getBestOne('GaussianProcesses')
MLP = MLP.MLP().getBestOne('MLP')
NearestNeighbors = NearestNeighbors.NearestNeighbors().getBstOne('NearestNeighbors')
RandomForest = RandomForest.RandomForest().getBestOne('RandomForest')
SGD = SGD.SGD().getBestOne('SGD')
SVC = SVC.SVC().getBestOne('SVC')
  
# final classifier
# finalClassifier = VotingClassifier(estimators=[
#        ('0', DecesionTree), ('1', ExtraTrees), ('2', GaussianNB), ('4', GaussianProcesses), ('6', MLP), ('7', NearestNeighbors), \
#         ('8', RandomForest), ('9', SGD)],  # ('5', SVC), ],
#        voting='soft')
finalClassifier = VotingClassifier(estimators=[
       ('0', DecesionTree), \
        ('1', ExtraTrees), ('2', SGD), ('4', SVC), \
         ('8', RandomForest)
        ],
       voting='soft')
  
# feature selection 
fetureSelection = SelectFromModel(DecesionTree)
clf = Pipeline([
('fetureSelection', fetureSelection),
  ('classification', DecesionTree)
])

# save the classifier as a dump
X, Y = DataCarer.createTrainDataSet()
accuracyRates = []
for i in range(1, 3):
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
    clf.fit(X_train, Y_train)
    accuracyRates.append(clf.score(X_test, Y_test))
    if i == 1:
        joblib.dump(clf, 'final.pkl')
        
# 输出正确率的均值
print(mat(accuracyRates).mean())
