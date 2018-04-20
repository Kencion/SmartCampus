'''
Created on 2018年4月12日

@author: xmu
'''
from background_program.b_Sample_processing.Feature_calculating import FeatureCalculater
import numpy as np
from background_program.y_Modules import score_forcasting
from background_program.b_Sample_processing.PreProcessing.GAN import Gan 
from numpy import mat
from sklearn.model_selection import train_test_split

class handleMissingData():
    def __init__(self):
        self.module=score_forcasting.score_forcasting()
        self.realdata = self.Get_Original_Data()#tuple:realdata
        self.nullIndexList=None
        self.tempdata=None
        self.nullIndexList=self.find_null_index(self.realdata)
        self.label=self.get_label()

    
    def get_label(self):
        
        dataset =FeatureCalculater.FeatureCalculater()
        sql='describe students_final'
        dataset.executer.execute(sql)
        labels=dataset.executer.fetchall()
        
        label1= []
        for i in labels:
            label1.append(i[0])

        return label1
        
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
#         tempdata=np.delete(xdata, nullIndexList, axis=1)
        return nullIndexList
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
        pp=0     
        for i in self.nullIndexList:
            label1=self.label.copy()
            label2=self.label.copy()
            pp+=1
            self.tempdata = np.copy(self.realdata)
            summ=0
            count=0
            for i2 in self.nullIndexList:
                if i2 != i:
                    for j1 in range(len(self.tempdata)):
                        if self.tempdata[j1,i2] != None:
                            summ +=self.tempdata[j1,i2]
                            count +=1
    
                    for j2 in range(len(self.tempdata)):
                        if self.tempdata[j2,i2] == None:
                            self.tempdata[j2,i2]=summ/float(count)
            
                
                        
#         for i in range(24,25):
            '''
            需要先找出第i列缺失的行下标
            '''
            print('*************************')
            defectRowIndex=[]
            defectRow=[]
            compeleteRow=[]
            for j in range(self.tempdata.shape[0]):
                if self.tempdata[j,i]==None:
                    defectRowIndex.append(j)
                    defectRow.append(self.tempdata[j])
#                     print(defectRow)
                else:
                    compeleteRow.append(self.tempdata[j])
#                     colunm_i.append([self.tempdata[j,i]])
            compeleteRow=np.array(compeleteRow)
            defectRow=np.array(defectRow)
            compeleteRow=np.hstack((compeleteRow,np.mat(compeleteRow[:,i]).T))
            label1.append(label1[i])
            compeleteRow=np.delete(compeleteRow,self.nullIndexList,axis=1)
            for uu in range(len(self.nullIndexList)):
                label1.pop(self.nullIndexList[len(self.nullIndexList)-1-uu])
            data_step1=compeleteRow
            data_step1=np.delete(data_step1, [0,1], axis=1)
            label1.pop(1)
            label1.pop(0)
            data_step1=np.array(data_step1)
            defectRow=np.delete(defectRow,self.nullIndexList,axis=1)
            for uu in range(len(self.nullIndexList)):
                label2.pop(self.nullIndexList[len(self.nullIndexList)-1-uu])
            defectRow=np.delete(defectRow,[0,1],axis=1)  
            label2.pop(1)
            label2.pop(0)

            
            print('(((((((')
            print(label1[len(label1)-1])
            print(len(label1))
            print(len(label2))
            print(')))))')
            print('*************************')
            '''
            先用gan网络生成数据
            '''
            print('---------------------------')
            ganitem=Gan.Gan()
            ganitem.all_data=data_step1
#             ganitem.all_data = ganitem.all_data.astype(float)
            ganitem.ART_COMPONENTS=ganitem.all_data.shape[1]
#             ganitem.run()
#             print(ganitem.final_gan_data[:,-1])
            print('---------------------------')
            
            '''
            将gan网络生成的数据与原表的子集合并成新表
            '''
            print('+++++++++++++++++++++++++++')
            Mixeddata=ganitem.all_data
#             Mixeddata=np.vstack((ganitem.all_data,ganitem.final_gan_data))
            print(Mixeddata.shape[0])
            print(Mixeddata.shape[1])
            X_train=mat(Mixeddata[:,:-1])
            Y_train=mat(Mixeddata[:,-1])
            Y_train=Y_train.T
#             print(Y_train)
#             print(X_train.shape[0])
#             print(X_train.shape[1])
#             print(Y_train.shape[0])
#             print(Y_train.shape[1])
            self.module.X_train, self.module.X_validate,self.module.Y_train, self.module.Y_validate = train_test_split(
                X_train, Y_train, test_size=0.2, random_state=3)
                
            self.module.X_train = mat(self.module.X_train, dtype=float)
            self.module.X_validate = mat(self.module.X_validate, dtype=float)
            self.module.Y_train = mat(self.module.Y_train, dtype=float)
            self.module.Y_validate = mat(self.module.Y_validate, dtype=float)
            self.module.X_test=mat(defectRow, dtype=float)
            
            evaluete_score, result=self.module.predict2()
            self.module.persistence_model()
            print(evaluete_score)
            print(result)
            print('+++++++++++++++++++++++++++')  
                
            '''
                    回填第i列(更新 realdata)
            '''
            index=0
            for j in defectRowIndex:
                self.realdata[j,i]=result[index]
                index +=1
            print(index-1)
            break
            
            
if __name__ == '__main__':
    test=handleMissingData()
    test.work()