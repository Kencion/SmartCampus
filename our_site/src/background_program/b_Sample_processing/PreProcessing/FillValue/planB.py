'''
Created on 2018年4月23日

@author: xmu

PlanB不会将存在缺失值的特征项用于预测

'''

from background_program.b_Sample_processing.Feature_calculating import FeatureCalculater
import numpy as np
from background_program.y_Modules import score_forcasting
from background_program.b_Sample_processing.PreProcessing.GAN import PlanB_gan 
from numpy import mat
from sklearn.model_selection import train_test_split
import random as RD


class PlanB():
    def __init__(self):
        self.module=score_forcasting.score_forcasting()
        self.realdata = self.Get_Original_Data()#tuple:realdata
        self.nullIndexList,self.tempdata=self.find_null_index(self.realdata)
          
    def find_null_index(self,xdata):
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
        return nullIndexList,tempdata
    # 
    # dataset =FeatureCalculater.FeatureCalculater()
    # dataset.executer.execute("select score from students_final where score is null")
    # result = dataset.executer.fetchall()
    # print(result)
    
    def Get_Original_Data(self):
        dataset =FeatureCalculater.FeatureCalculater()
        sql='select * from students_final'
        dataset.executer.execute(sql)
        original_data=dataset.executer.fetchall()
        original_data=np.array(original_data)
        return original_data

    
    
    def work(self):   
#         for i in self.nullIndexList:            
        for i in range(24,25):
            '''
            需要先找出第i列缺失的行下标
            '''
            print('*************************')
            defectRowIndex=[]
            defectRow=[]
            compeleteRow=[]
            colunm_i=[]
            print(i)
            for j in range(self.realdata.shape[0]):
                if self.realdata[j,i]==None:
                    defectRowIndex.append(j)
                    defectRow.append(self.tempdata[j])
                else:
                    compeleteRow.append(self.tempdata[j])
                    colunm_i.append([self.realdata[j,i]])
                    
            colunm_i=np.array(colunm_i)
            compeleteRow=np.array(compeleteRow)
            compeleteRow=np.hstack((compeleteRow,colunm_i))
            compeleteRow=np.delete(compeleteRow, [0,1], axis=1)
            
            listy=[]
            defectRow=np.array(defectRow)
            for kk in range(defectRow.shape[0]):
#                 listy.append([(RD.uniform(0,5)+1)/2])
                listy.append([70])
            listy=np.array(listy)
            defectRow=np.hstack((defectRow,listy))
            defectRow=np.delete(defectRow, [0,1], axis=1)
            print('*************************')
            '''
            先用gan网络生成数据
            '''
            print('---------------------------')
            ganitem=PlanB_gan.GanB()
            ganitem.all_data=compeleteRow
            ganitem.ART_COMPONENTS=ganitem.all_data.shape[1]
            ganitem.N_IDEAS=ganitem.ART_COMPONENTS
            ganitem.noise=defectRow
            ganitem.MINIBATCH_SIZE =defectRow.shape[0]
            ganitem.run()
#             print(ganitem.final_gan_data[:,-1])
             
            dataset =FeatureCalculater.FeatureCalculater()
            liat=[]
            for xh in range(defectRow.shape[0]):
                liat.append(int(ganitem.final_gan_data[xh,-1])-int(int((ganitem.final_gan_data[xh,-1]))/100)*100)
#                 print(int(ganitem.final_gan_data[xh,-1]))
#                 print(int(int((ganitem.final_gan_data[xh,-1]))/100)*100)
#                 print(liat[xh])
                sql='update students_final set score = {0} where student_num= "{1}"'
#                 print(sql.format(round(float(defectRow[xh,-1]),3),str(self.realdata[defectRowIndex[xh],0])))
#                 dataset.executer.execute(sql.format(int((defectRow[xh,-1]))/100*100,str(self.realdata[defectRowIndex[xh],0])))
# #             print(ganitem.final_gan_data[:,-1])
            print('---------------------------')
            
            max = 10
            min = 30
            for xh in range(len(liat)):
                if max <liat[xh]:
                    max=liat[xh]
               
# #             print(max)
#             print(min)
            for xh in range(len(liat)):
                print(liat[xh])
                liat[xh]=liat[xh]-min
                if liat[xh]<0:
                    liat[xh]=abs(liat[xh])+RD.uniform(0,10)
                liat[xh]=(liat[xh]/(max-min-5))*100
                print(liat[xh])
                sql='update students_final set score = {0} where student_num= "{1}"'
#                 print(sql.format(round(float(defectRow[xh,-1]),3),str(self.realdata[defectRowIndex
                dataset.executer.execute(sql.format(liat[xh],str(self.realdata[defectRowIndex[xh],0])))

        
#             '''
#             将gan网络生成的数据与原表的子集合并成新表
#             '''
#             print('+++++++++++++++++++++++++++')
# #             Mixeddata=ganitem.all_data
#             Mixeddata=np.vstack((ganitem.all_data,ganitem.final_gan_data))
#             print(Mixeddata.shape[0])
#             print(Mixeddata.shape[1])
#             X_train=mat(Mixeddata[:,:-1])
#             Y_train=mat(Mixeddata[:,-1])
#             Y_train=Y_train.T
# #             print(Y_train)
# #             print(X_train.shape[0])
# #             print(X_train.shape[1])
# #             print(Y_train.shape[0])
# #             print(Y_train.shape[1])
#             self.module.X_train, self.module.X_validate,self.module.Y_train, self.module.Y_validate = train_test_split(
#                 X_train, Y_train, test_size=0.2, random_state=3)
#                 
#             self.module.X_train = mat(self.module.X_train, dtype=float)
#             self.module.X_validate = mat(self.module.X_validate, dtype=float)
#             self.module.Y_train = mat(self.module.Y_train, dtype=float)
#             self.module.Y_validate = mat(self.module.Y_validate, dtype=float)
#             self.module.X_test=mat(defectRow, dtype=float)
#             
#             evaluete_score, result=self.module.predict2()
#             print(evaluete_score)
#             print(result)
#             print('+++++++++++++++++++++++++++')  
#                 
#             '''
#                     回填第i列(更新 realdata)
#             '''
#             index=0
#             for j in defectRowIndex:
#                 self.realdata[j,i]=result[index]
#                 index +=1
#             print(index-1)
#             self.tempdata=np.hstack((self.tempdata,mat(self.realdata[:,i])))
            
            
            
if __name__ == '__main__':
    test=PlanB()
    test.work()