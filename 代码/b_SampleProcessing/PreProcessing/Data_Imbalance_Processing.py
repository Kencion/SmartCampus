'''
Created on 2017年11月29日

@author: LENOVO
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
from boto.sdb.db.sequence import double
import random
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sqlalchemy.orm.relationships import remote
from statsmodels.stats.proportion import proportion_confint

class Data_Imbalance_Processing(FeatureCalculater):
    def __init__(self,samples,N=10,k=5):
        FeatureCalculater.__init__(self)
        self.n_samples,self.n_attrs=samples.shape#获取样本数和属性个数
        self.N=N#根据样本不平衡比例设置一个采样比例以确定采样倍率N
        self.k=k#k邻近个点
        self.samples=samples
        self.newindex=0
    def over_sampling(self):
        #N=int(self.N)#设置样本的采样倍率
        N=1
        self.synthetic = np.zeros((self.n_samples * N, self.n_attrs))#初始化采样样本集
        neighbors=NearestNeighbors(n_neighbors=self.k).fit(self.samples)
        for i in range(len(self.samples)):
            #reshape：-1代表Numpy会根据剩下的维度计算出数组的另外一个shape属性值。
            nnarray=neighbors.kneighbors(self.samples[i].reshape(1,-1),return_distance=False)[0]
            self._populate(N,i,nnarray)
        return self.synthetic
    def _populate(self,N,i,nnarray):
        for j in range(N):
            nn=random.randint(0,self.k-1)
            dif=self.samples[nnarray[nn]]-self.samples[i]
            gap=random.random()
            self.synthetic[self.newindex]=self.samples[i]+gap*dif
            self.newindex+=1
    def _get_proportion(self,feature):
        sql="select count(*) from students"
        self.executer.execute(sql)
        total_num=self.executer.fetchone()[0]
        sql="select "+feature+",count(*) from students group by "+feature+""
        self.executer.execute(sql)
        result=self.executer.fetchall()
        #print(result)
        lists = [[] for i in range(len(result))]
        list=[]
        list2=[]
        for i in range(len(result)):
            lists[i].append(result[i][0])
            lists[i].append(float(result[i][1])/float(total_num))
            list.append(result[i][1])
            list2.append(result[i][0])
        list=sorted(list)
        proportion=round(float(max(list))/3.0)-min(list)
        return lists,proportion#lists表示各类别以及所占比例，proportion表示需要其他类别增加的数量
    def _get_samples(self,feature,value):
        sql="select * from students where {0}={1}"
        self.executer.execute(sql.format(feature, value))
        samples=self.executer.fetchall()
        sql="select count(*) from students where {0}={1}"
        self.executer.execute(sql.format(feature, value))
        num=self.executer.fetchone()[0]
        return samples,num
    def _get_data(self,lists,proportion,feature):
        lists=sorted(lists, key=lambda x:x[1])#根据各类别比例排序
        del lists[-1]#删除所占比例最大的元素，因为他不需要你在进行增加样本数
        for i in range(len(lists)):
            samples,num=self._get_samples(feature, lists[i][0])#获取某个类别的样本特征数据集
            samples=list(samples)
            samples=np.array(samples)#将元组转换为nparray
            dip2=Data_Imbalance_Processing(samples,round(float(proportion)/num))
            new_dataSet=dip2.over_sampling()#新生成的样本集
            print(new_dataSet)
#             for re in new_dataSet:
#                 sql="insert into students_rank values(%s,%s,%s,%s)"#需要插入的字段
#                 self.executer.execute(sql.format(re[0],re[1],re[2],re[3]))
if __name__=='__main__':
    a=np.array([[1,2,3],[4,5,6],[2,3,1],[2,1,2],[2,3,4],[2,3,4]])#没有用的数据，单纯生成对象参数
    dip=Data_Imbalance_Processing(a,N=100)
    lists,proportion=dip._get_proportion('score')#分类属性
    dip._get_data(lists, proportion,'score')