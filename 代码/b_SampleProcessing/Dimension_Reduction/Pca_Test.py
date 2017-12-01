from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
from boto.sdb.db.sequence import double
import numpy as np
from sklearn.decomposition import PCA
class Pca_Test(FeatureCalculater): 
    def get_traindataSet(self):
        sql = "select activity_num,activity_avg_level,participation_avg_point,hornorary_times,library_borrow_times,library_study_time from students where activity_num!=0"
        self.executer.execute(sql)
        samples = self.executer.fetchall()
        samples=list(samples)
        samples=np.array(samples)#将元组转换为nparray
        return samples
    def get_testdataSet(self):
        sql = "select activity_num,activity_avg_level,participation_avg_point,hornorary_times,library_borrow_times,library_study_time from students where activity_num!=0"
        self.executer.execute(sql)
        samples = self.executer.fetchall()
        samples=list(samples)
        samples=np.array(samples)#将元组转换为nparray
        return samples
    def Train_dataSet(self,samples,n):  
        self.pca=PCA(n_components=n,copy=True, whiten=False)
        newData=self.pca.fit_transform(samples,'mle') 
        print(newData)
    def Test_dataSet(self,samples): 
        newData=self.pca.transform(samples)
    def zeroMean(self,dataMat):      #零均值化       
        meanVal=np.mean(dataMat,axis=0)     #按列求均值，即求各个特征的均值  
        newData=dataMat-meanVal 
        newData /= np.std(newData+ 1e-5, axis = 0) # 归一化,归一化以后数据X就被归一化到-1到1的范围内 
        return newData,meanVal  
      
    def pca_2(self,dataMat,percentage=0.99):  
        newData,meanVal=self.zeroMean(dataMat)  
        covMat=np.cov(newData,rowvar=0)    #求协方差矩阵,return ndarray；若rowvar非0，一列代表一个样本，为0，一行代表一个样本  
        eigVals,eigVects=np.linalg.eig(np.mat(covMat+1e-5))#求特征值和特征向量,特征向量是按列放的，即一列代表一个特征向量  
        n=self.percentage2n(eigVals,percentage)                 #要达到percent的方差百分比，需要前n个特征向量  
        return n
    
    def percentage2n(self,eigVals,percentage):  
        sortArray=np.sort(eigVals)   #升序  
        sortArray=sortArray[-1::-1]  #逆转，即降序  
        arraySum=sum(sortArray)  
        tmpSum=0  
        num=0  
        for i in sortArray:  
            tmpSum+=i  
            num+=1  
            if tmpSum>=arraySum*percentage:  
                return num
if __name__=='__main__':
    print("begin......")
    p=Pca_Test()
    samples=p.get_traindataSet()
    n=p.pca_2(samples,0.99) 
    samples2=p.get_testdataSet()
    p.Train_dataSet(samples, n)
    p.Test_dataSet(samples2)
    print("Over......") 
