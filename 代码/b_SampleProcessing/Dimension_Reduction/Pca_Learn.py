from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
from boto.sdb.db.sequence import double
import Pca_Test
import numpy as np 
class Pca_Learn(FeatureCalculater): 
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
    
if __name__=='__main__':
    pca2=Pca_Learn()
    samples=pca2.get_traindataSet()
    pca =Pca_Test.Pca_Test()
    n=pca.pca_2(samples,0.99) 
    samples2=pca2.get_testdataSet()
    #pca.Train_dataSet(samples2, n)
    pca.Train_dataSet(samples, n)
    pca.Test_dataSet(samples2)