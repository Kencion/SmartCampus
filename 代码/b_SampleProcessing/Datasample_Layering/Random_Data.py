# -*- coding:utf-8 -*-
import numpy as np
import random
 
class Random_Data(object):
    def __init__(self):
        pass
     
    def group(self, data_set, label, percent=0.1):
        list=np.zeros([len(label)])
        train_data,test_data=[],[]
        data_set=np.array(data_set)
        lists = [[] for i in range(len(label))]
        #优化代码，降低时间复杂度，label是类别个数
        for re in data_set:#统计各类的数目
            count=0
            for i in range(len(label)):
                if float(re[-1])==float(label[i]):
                    list[i]+=1
                    lists[count].append(re)
                count+=1
        for i in range(len(list)):#计算各类抽样数目
            list[i]=int(round(float(list[i])*(1-percent)))
        for i in range(len(label)):
            if round(float(list[i]))!=0:
                train_data.extend(self.group_traindata_sample(lists[i],list[i]))
                test_data.extend(self.group_testdata_sample(lists[i]))
        train_data=np.array(train_data)  
        return train_data,test_data
     
    def group_traindata_sample(self,list,count):#提取训练集
        result=[]
        for i in range(len(list)):
            num=random.randint(0, int(len(list)-1))
            result.append(list[num])
            list.pop(num)
            count-=1
            if int(count)==0:
                break
        return result
     
    def group_testdata_sample(self,list): #提取验证集
        result=list
        return result 