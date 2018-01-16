'''
Created on 2017年11月29日
   
@author: yhj
'''
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
import random
from sklearn.neighbors import NearestNeighbors
import numpy as np
   
class Data_Imbalance_Processing(FeatureCalculater):
    """
            类的构造器函数，初始化一些参数
    @params（参数列表）nparray samples:完整的样本集(剔除学号字段，不能包含非数值型字段)
    int N:采样倍率N(根据最少类)
    int K：k邻近个点
    """
    def __init__(self,samples,N=10,k=1):
        FeatureCalculater.__init__(self)
        self.n_samples,self.n_attrs=samples.shape#获取样本数和属性个数
        self.N=N#根据样本不平衡比例设置一个采样比例以确定采样倍率N
        self.k=k#k邻近个点
        self.samples=samples
        self.newindex=0
    """
            数据过采样处理函数(根据KNN算法的思想，求k邻近点)
    @retrun（返回值解释） nparray self.synthetic:新增加的样本集
    """
    def over_sampling(self):
        N=int(self.N)#设置样本的采样倍率
        self.synthetic = np.zeros((self.n_samples * N, self.n_attrs))#初始化采样样本集
        neighbors=NearestNeighbors(n_neighbors=self.k).fit(self.samples)
#         print("*******************")
#         print(self.samples)
        for i in range(len(self.samples)):
            #reshape：-1代表Numpy会根据剩下的维度计算出数组的另外一个shape属性值。
            nnarray=neighbors.kneighbors(self.samples[i].reshape(1,-1),return_distance=False)[0]
            self._populate(N,i,nnarray)
#             print("***************")
#             print(nnarray)
        return self.synthetic
    """
            根据规则生成新样本集的函数
    @params（参数列表）nparray nnarray:根据KNN求出的k个点标签在样本集中的下标
    int N:采样倍率N(根据最少类)
    int i：参数
    """
    def _populate(self,N,i,nnarray):#问题
        for j in range(N):
            nn=random.randint(0,self.k-1)
            nnarray[nn].astype('int') 
            dif=self.samples[nnarray[nn]]-self.samples[i]
            gap=random.random()
            self.synthetic[self.newindex]=self.samples[i]+gap*dif
            self.newindex+=1
    """
            根据分类标签，统计各类别所占比例，获取低比例样本需要增加的样本数量
    @params（参数列表）字符型串 feature:分类标签的特征字段名
    @retrun（返回值解释） list lists:表示各类别以及所占比例
    int proportion：表示需要其他类别增加的数量
    """
    def _get_proportion(self,feature):
        sql="select count(*) from students_rank"
        self.executer.execute(sql)
        total_num=self.executer.fetchone()[0]
        sql="select "+feature+",count(*) from students_rank group by "+feature+""
        self.executer.execute(sql)
        result=self.executer.fetchall()
        lists = [[] for i in range(len(result))]
        list=[]
        list2=[]
        for i in range(len(result)):
            lists[i].append(result[i][0])
            lists[i].append(float(result[i][1])/float(total_num))
            list.append(result[i][1])

        list=sorted(list)
        proportion=round(float(max(list))/3.0)-min(list)
        return lists,proportion#lists表示各类别以及所占比例，proportion表示需要其他类别增加的数量
    """
            根据分类标签，分类标签字段所取的值，计算该类别所占的数量和该类别的样本集
    @params（参数列表）字符型串 feature:分类标签的特征字段名
           （  int,float） value:分类标签所取的值
    @retrun（返回值解释） list samples:该类别的样本集 (剔除学号字段)
    int num:该类别样本所占的数量
    """
    def _get_samples(self,feature,value):
        sql="select * from students_rank where {0}={1}"
        self.executer.execute(sql.format(feature, value))
        samples=self.executer.fetchall()
        sql="select count(*) from students_rank where {0}={1}"
        self.executer.execute(sql.format(feature, value))
        num=self.executer.fetchone()[0]
        samples=[i[1:] for i in samples]
        return samples,num
    """
            对于增加样本的方法后期还可以完善，目前操作比较粗糙
            获取新样本数据集函数
    @params（参数列表）字符型串 feature:分类标签的特征字段名
    int proportion:表示需要其他类别增加的数量
    list lists:表示各类别以及所占比例
    @retrun（返回值解释） nparray new_dataSet:获取的新样本总集合
    """
    def _get_data(self,lists,proportion,feature):
        lists=sorted(lists, key=lambda x:x[1])#根据各类别比例排序
        del lists[-1]#删除所占比例最大的元素，因为他不需要你在进行增加样本数
        n=1
        for i in range(len(lists)):
            samples,num=self._get_samples(feature, lists[i][0])#获取某个类别的样本特征数据集
            samples=list(samples)
            samples=np.array(samples)#将元组转换为nparray
            dip2=Data_Imbalance_Processing(samples,round(float(proportion)/num),4)
            dataSet=dip2.over_sampling()#新生成的样本集
            if n==1:
                new_dataSet=dataSet
                n+=1
            else:
                new_dataSet = np.vstack((new_dataSet, dataSet))
        return new_dataSet
if __name__=='__main__':
    a=np.array([[1,2,3],[4,5,6],[2,3,1],[2,1,2],[2,3,4],[2,3,4]])#没有用的数据，单纯生成对象参数
    dip=Data_Imbalance_Processing(a,N=100)
    lists,proportion=dip._get_proportion('score')#分类属性
    dip._get_data(lists, proportion,'score')