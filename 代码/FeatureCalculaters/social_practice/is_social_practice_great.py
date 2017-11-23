'''
Created on 2017年11月23日

@author: yzh
'''

from Tools import *
from FeatureCalculaters import FeatureCalculater

class score_rank1(FeatureCalculater.FeatureCalculater):
    '''
            判断是否是院级或者校级重点。
            思路：从social_practice表中获取student_num以及学年（根据start_time来划分），是否是重点，然后根据stu_num关键字填入students表中。
    '''
    def setLevel(self):
        pass
    
    def calculate(self):
        sql = "select stu_num,DATE_FORMAT(start_time,'%Y'),DATE_FORMAT(start_time,'%c'),School_key_projects_or_not,College_key_projects_or_not from social_practice"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            year = int(i[1])
            month = int(i[2])
            #print("month = "+str(month))
            if(month<9):
                year = year - 1
            School_key_projects_or_not = i[3]
            College_key_projects_or_not = i[4]
            if(School_key_projects_or_not == "否" and College_key_projects_or_not =="否"):
                is_social_practice_great = 0
            else:
                is_social_practice_great = 1
            sql = "update students set is_social_practice_great = '"+str(is_social_practice_great)+"' where student_num = '"+str(stu_num)+str(year)+"'"
            #print(sql)
            self.executer.execute(sql)
            
    @MyLogger.myException
    def rankit(self):
        pass