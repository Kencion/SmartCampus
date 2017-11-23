'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class library_week_study_time(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                        计算每一学年周末图书馆学习时间
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            sql = "SELECT sum(seat_time) FROM library_study_time where student_num =' " + student_num + "' AND DAYOFYEAR(select_seat_time)= " + str(school_year) + " AND DAYOFWEEK(select_seat_time) in (6,7)"
            self.executer.execute(sql)
            library_week_study_time = self.executer.fetchone()[0]
            if library_week_study_time == None:
                library_week_study_time = 0
            sql = "update students set library_week_study_time =" + str(library_week_study_time) + " where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
        
    @MyLogger.myException
    def rankit(self):
        pass
