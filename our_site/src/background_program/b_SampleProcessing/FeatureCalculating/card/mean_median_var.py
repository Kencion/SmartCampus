'''
Created on 2017年12月19日

@author: LI
'''
import numpy as np
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
from numpy.core.numeric import NaN
import sys

class mean_median_var(FeatureCalculater):
   
    def calculate(self):
        '''
                获取最早时间、最晚时间
        '''
        sql = 'select min(date),max(date) from card'
        self.executer.execute(sql)
        result = self.executer.fetchone()
        earliestItem_date = result[0]
        lastestItem_date = result[1]  
#         print(earliestItem_date,lastestItem_date)
#         print(type(earliestItem_date),type(lastestItem_date))
        
        '''
                获得 'card' 表中包含的学年
                eg: 2014-06-04应该属于2013-2014学年
                    2015-09-03应该属于2015-2016学年
        '''
        school_year =[]
        eyear =int(earliestItem_date.year)
        if earliestItem_date.month < 9 :
            eyear = eyear-1
            
        lyear =lastestItem_date.year
        if lastestItem_date.month < 9 :
            lyear = lyear-1
        
        while eyear <=lyear :
            school_year.extend([eyear])
            eyear = eyear+1  
         
        '''
                获得 'card' 表中包含的student_num的集合
                存放在student_num_list中
        '''    
        sql = 'select distinct student_num from card' 
        self.executer.execute(sql)
        student_num_list=self.executer.fetchall()
        
        '''
                获得所有的消费类型
                存放在type_list中
        '''
        sql = 'select distinct type from card' 
        self.executer.execute(sql)
        type_list=self.executer.fetchall()
#         print(type_list)
        
        for student_num in student_num_list:
            for one_type in type_list:
                for year in school_year:
                    sql = 'select abs(transaction_amount) from card where student_num = "'"{0}"'" and ((year(date)={1} and month(date)>8) or (year(date)={2} and month(date)<9)) and type="'"{3}"'"'
                    self.executer.execute(sql.format(student_num[0],int(year),int(year)+1,one_type[0]))
                    result = self.executer.fetchall()
                    mean,median,var=self.get_result(result)
                    
                    '''
                    mean,median,var 非nan 才更新
                    '''
                    if np.isnan(mean)==False : 
                        mean,median,var =round(mean,3),round(median,3), round(var,3)
                        sql = 'update students set {1}={2},{3}={4},{5}={6} where student_num ="'"{0}"'"'
#                         print(sql.format(str(student_num[0])+str(year),"mean_of_"+str(one_type[0]),mean,"median_of_"+str(one_type[0]),median,"var_of_"+str(one_type[0]),var))
                        self.executer.execute(sql.format(str(student_num[0])+str(year),"mean_of_"+str(one_type[0]),mean,"median_of_"+str(one_type[0]),median,"var_of_"+str(one_type[0]),var))
                  
        
        
    '''
        计算并返回输入参数 'datalist' 的平均值、中位数、方差 
    @param :
        datalist: 1d_array-like ，shape(n_items) ,the original data  
    @return : 
        result(list): [平均值、中位数、方差]
    '''
    def get_result(self,datalist):
        mean = np.mean(datalist)
        median = np.median(datalist)
        var = np.var(datalist)
        
        return mean,median,var
    

test =mean_median_var()
test.calculate()
    