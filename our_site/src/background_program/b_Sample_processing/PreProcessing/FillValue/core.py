'''
Created on 2018年4月12日

@author: xmu
'''
from background_program.b_Sample_processing.Feature_calculating import FeatureCalculater
import numpy as np
from background_program.y_Modules import score_forcasting
from background_program.b_Sample_processing.PreProcessing.GAN import Gan
def find_null_index(xdata):
    '''
    xdata: 输入数据集
    @return nullIndexList xdata 中 含有null的列下标
    '''
    nullIndexList=[]
    xdata=np.array(xdata)
   
    dataset =FeatureCalculater.FeatureCalculater()
    sql='describe students_final'
    dataset.executer.execute(sql)
    labels=dataset.executer.fetchall()
    
       
    for i in range(xdata.shape[1]):
        for j in range(xdata.shape[0]):
            if xdata[j,i]==None:
                nullIndexList.append(i)
                print(labels[i][0])
                break
            pass
    tempdata=np.delete(xdata, nullIndexList, axis=1)
    return tempdata,nullIndexList
# 
# dataset =FeatureCalculater.FeatureCalculater()
# dataset.executer.execute("select score from students_final where score is null")
# result = dataset.executer.fetchall()
# print(result)

def Get_Original_Data():
    dataset =FeatureCalculater.FeatureCalculater()
    sql='select * from students_final'
    dataset.executer.execute(sql)
    original_data=dataset.executer.fetchall()
    return original_data

realdata = Get_Original_Data()#tuple:realdata
tempdata,nullIndexList=find_null_index(realdata)
realdata=np.array(realdata)


'''
获取预测模型
'''
module=score_forcasting()


for i in nullIndexList:
    '''
    需要先找出第i列缺失的行下标
    '''
    defectRow=[]
    for j in range(realdata.shape[0]):
        if realdata[j,i]==None:
            defectRow.append(j)
    
    
    '''
    先用gan网络生成数据
    '''
    ganitem=Gan()
    ganitem.
    
#      
        
    