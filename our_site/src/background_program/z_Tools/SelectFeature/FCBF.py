'''
Created on 2018年4月3日
@author: YHJ
'''
from background_program.z_Tools.SelectFeature import features_name
from background_program.a_Data_prossing import DataCarer
import math
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
class FCBF():
    def __init__(self):
        pass
    '''
        FCBF-NMI算法逻辑实现
        @params X_train（不包含非数值型特征，离散化） np.array类型 Y_train np.array类型           
        @retrun Feature_Names list 筛选后的特征属性名
        Feature_Values_pandas pandas.dataframe 筛选后剩余的属性名称和对应的属性值 训练集
        Feature_Values_np np.array 筛选后剩余属性特征值 训练集
        '''
    def FCBF_realize(self,X_train,Y_train):
        #从制定文件获取属性名称，存为columns=["a","b","c"]形式
        #获取的属性列不包括类标签和非数值型特征(student_type,student_num)
        columns=features_name.fea_name
        F=np.array(X_train.T)#初始化F
        data = DataFrame(X_train,columns=columns)
        #根据列名称或者下标删除对应的列
#         data.drop('a',axis=1, inplace=True)
#         data.drop([data.columns[0]],axis=1, inplace=True)
        NMI=[]
        t=-10000.0
        for x in F:
            #计算每个属性特征与类别的归一化信息
            NMI.append(self.calcute_NMI(x, Y_train))
        #data保留的是>t的属性数组
        tag=0
        for i in range(len(NMI)):
            if NMI[i]<=t:
                data.drop([data.columns[tag]],axis=1, inplace=True)
                tag=tag-1
            tag=tag+1
        S_result=DataFrame(data[data.columns[0]],columns=["j"])
        while data.columns.size!=0:
            Y=np.array(data[data.columns[0]])
            S_result2=DataFrame(data[data.columns[0]],columns=[data.columns[0]])
            S_result=pd.concat([S_result,S_result2],axis=1)
            data.drop([data.columns[0]],axis=1, inplace=True)
            for i in range(data.columns.size):
                if i<data.columns.size:
                    nmi=self.calcute_NMI(Y, np.array(data[data.columns[i]]))
                    nmi_2=self.calcute_NMI(np.array(data[data.columns[i]]), Y_train)
                    if nmi>nmi_2:
                        data.drop([data.columns[i]],axis=1, inplace=True)
        S_result.drop('j',axis=1, inplace=True)
        #获取pandas的属性列名称
        Feature_Names=list(S_result.columns)
        Feature_Values_pandas=S_result
        Feature_Values_np=np.array(S_result)
        print(Feature_Names)
        return Feature_Names,Feature_Values_pandas,Feature_Values_np
            
    #计算每个属性与类标签之间的归一化互信息NMI的值
    #特征标签都要离散化
    def calcute_NMI(self,X_train,Y_train):
        #样本点数
        X_train=X_train.T
#         for x in X_train:
        total =len(X_train)
        A_ids = set(X_train)
        B_ids = set(Y_train)
        #互信息计算
        MI = 0
        eps = 1.4e-45
        for idA in A_ids:
            for idB in B_ids:
                idAOccur = np.where(X_train==idA)
                idBOccur = np.where(Y_train==idB)
                idABOccur = np.intersect1d(idAOccur,idBOccur)
                px = 1.0*len(idAOccur[0])/total
                py = 1.0*len(idBOccur[0])/total
                pxy = 1.0*len(idABOccur)/total
                MI = MI + pxy*math.log(pxy/(px*py)+eps,2)
         # 标准化互信息
        mini=min(math.log(len(A_ids),2)+eps,math.log(len(B_ids),2)+eps)
        NMI=MI/mini
        return NMI
if __name__=="__main__":
    import datetime
    fcbf=FCBF()
    dc=DataCarer.DataCarer('scholarship_amount','2016',"classification")
    X_train, Y_train=dc.create_train_dataSet()
    X_train=np.array(X_train)
#     X_train=np.array([[1,2,3,4,1,1],[2,3,3,3,1,1],[1,4,5,3,1,1],[1,2,3,4,1,1],[2,3,3,3,1,1],[1,4,5,3,1,1],[1,1,3,3,4,4],[2,0,1,2,3,4]])
#     Y_train=np.array([1,2,4,1,2,4,2,1])
    
    #将Y_train转换为一维的nparray类型
    Y_train=np.array(Y_train).reshape(len(Y_train),)
    Feature_Names,Feature_Values_pandas,Feature_Values_np=fcbf.FCBF_realize(X_train, Y_train)
#     print(Feature_Values_pandas)
    #将Y_train重新转换为二维的nparray类型
    Y_train=np.array(Y_train).reshape(len(Y_train),1)