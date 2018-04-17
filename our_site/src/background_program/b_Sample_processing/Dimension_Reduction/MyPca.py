import numpy as np
from sklearn.decomposition import PCA
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater

class MyPca(FeatureCalculater): 
    
    def __init__(self, X_train):
        n = self.pca_2(X_train, 0.99)
        self.pca = PCA(n_components=n, copy=True, whiten=False)
    
    def Train_dataSet(self, samples, n):  
        """
                          将训练数据集降维并根据训练集获取PCA模型，用于测试集降维
        @params（参数列表）nparray samples:特征提取后的训练样本集，int n:降维后的样本维度
        @retrun（返回值解释） nparray newData:降维后的训练样本集合
        """
        newData = self.pca.fit_transform(samples, n)  # 'mle'表示算法自己判断需要降维几维，n是我们计算出来的维度
        return newData
    
    def Test_dataSet(self, samples): 
        """
                          根据训练集获取PCA模型,对测试集进行降维操作
        @params（参数列表）nparray samples:特征提取后的训练样本集
        @retrun（返回值解释） nparray newData:降维后的测试样本集合
        """
        newData = self.pca.transform(samples)
        return newData
    
    def zeroMean(self, dataMat):  # 零均值化       
        """
                        数据零均值化和归一化处理函数
        @params（参数列表）nparray dataMat:训练数据样本集
        @retrun（返回值解释） nparray  newData:归一化后的训练样本集
        nparray meanVal:；列均值
        """    
        meanVal = np.mean(dataMat, axis=0)  # 按列求均值，即求各个特征的均值  
        newData = dataMat - meanVal 
        newData /= np.std(newData + 1e-5, axis=0)  # 归一化,归一化以后数据X就被归一化到-1到1的范围内 
        return newData, meanVal  
    
    def pca_2(self, dataMat, percentage=0.99):  
        """
                        根据训练数据集和百分比计算特征向量和特征值集合，传递给percentage2n（），返回n
        @params（参数列表）nparray dataMat:训练数据样本集
        float percentage:百分比，
        @retrun（返回值解释） int  num:需要降成的维度
        """
        newData, meanVal = self.zeroMean(dataMat) 
        covMat = np.cov(newData, rowvar=0)  # 求协方差矩阵,return ndarray；若rowvar非0，一列代表一个样本，为0，一行代表一个样本  
        eigVals, eigVects = np.linalg.eig(np.mat(covMat + 1e-5))  # 求特征值和特征向量,特征向量是按列放的，即一列代表一个特征向量  
        n = self.percentage2n(eigVals, percentage)  # 要达到percent的方差百分比，需要前n个特征向量  
        return n
    
    def percentage2n(self, eigVals, percentage):  
        """
                        根据特征值和设定的百分比求降维的后的维度n
        @params（参数列表）nparray eigVals:根据特征数据集得出的特征值集合；float percentage:百分比，
        @retrun（返回值解释） int  num:需要降成的维度
        """
        sortArray = np.sort(eigVals)  # 升序  
        sortArray = sortArray[-1::-1]  # 逆转，即降序  
        arraySum = sum(sortArray)  
        tmpSum = 0  
        num = 0  
        for i in sortArray:  
            tmpSum += i  
            num += 1  
            if tmpSum >= arraySum * percentage:  
                return num