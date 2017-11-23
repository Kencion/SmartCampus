'''
Created on 2017年11月23日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class avg_hornorary_times(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年内获得荣誉次数
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select count(*) from hornorary_handled where student_num=%s and grant_year=%s", (student_num, school_year + "-" + str(int(school_year) + 1)))
            avg_hornorary_times = self.executer.fetchone()[0]
            print(avg_hornorary_times)
            self.executer.execute("update students set avg_hornorary_times =%s where student_num=%s" , (avg_hornorary_times, student_num + school_year))
        
    @MyLogger.myException
    def rankit(self):
        pass
