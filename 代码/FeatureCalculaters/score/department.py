'''
Created on 2017年11月23日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class department(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                        计算学生的系别
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select department from score where student_num=%s", (student_num))
            department = self.executer.fetchone()[0]
            self.executer.execute("update students set hornorary_rank =%s where student_num=%s" , (department, student_num + school_year))
        
    @MyLogger.myException
    def rankit(self):
        pass
