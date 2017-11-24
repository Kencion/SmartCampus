'''
Created on 2017年11月24日

@author: LENOVO
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
from numpy import float16, double
from sklearn.cluster import KMeans
import numpy
class score(FeatureCalculater.FeatureCalculater):
    def Calcute_score(self):
        dataSet = []
        sql="select score from students where score!=0"
        count=self.executer.execute(sql)
        result=self.executer.fetchall()
        for re in result:
            dataSet.append(re[0])#根据数据库表中的字段取精度
        #调用sklearn.cluster中的KMeans类
        dataSet = numpy.array(dataSet).reshape(count,1)
        kmeans = KMeans(n_clusters=4, random_state=0).fit(dataSet)#聚类的个数
        clusters=4
        #求出聚类中心
         #print(dataSet)
        center=kmeans.cluster_centers_
        center_x=[]
        #center_y=[]
        for i in range(len(center)):
            center_x.append('%0.4f' % center[i][0])
           # center_y.append('%0.6f' % center[i][1])
        print(center_x)
        #标注每个点的聚类结果
        labels=kmeans.labels_ 
        type1_x = []
        type2_x = []
        type3_x = []
        type4_x = []
         #print(type(type1_x))
        max2=[]
        min2=[]
         #print(str(labels[0]+1))
        for i in range(len(labels)):
            if labels[i] == 0:
                type1_x.append(dataSet[i][0])
                sql="update students_rank set score='"+str(labels[i]+1)+"' where score='"+str(dataSet[i][0])+"'"
                self.executer.execute(sql)
            if labels[i] == 1:
                type2_x.append(dataSet[i][0])
                sql="update students_rank set score='"+str(labels[i]+1)+"' where score='"+str(dataSet[i][0])+"'"
                self.executer.execute(sql)
            if labels[i] == 2:
                type3_x.append(dataSet[i][0])
                sql="update students_rank set score='"+str(labels[i]+1)+"' where score='"+str(dataSet[i][0])+"'"
                self.executer.execute(sql)
            if labels[i] == 3:
                type4_x.append(dataSet[i][0])
                sql="update students_rank set score='"+str(labels[i]+1)+"' where score='"+str(dataSet[i][0])+"'"
                self.executer.execute(sql)
        
        max2.append(max(type1_x))
        min2.append(min(type1_x))
        max2.append(max(type2_x))
        min2.append(min(type2_x))
        max2.append(max(type3_x))
        min2.append(min(type3_x))
        max2.append(max(type4_x))
        min2.append(min(type4_x))
        with open(r"聚类对应的字段区间","a",encoding='utf8') as f:
            f.write('score字段'+'\n')
            for i in range(len(center)):
                f.write(str(i)+':'+' '+str(center[i][0])+' '+str(min2[i])+' '+str(max2[i])+'\n')
            f.close()
         #print(max2)
         #print(min2)
        #max3=sorted(max2)
        #min3=sorted(min2)