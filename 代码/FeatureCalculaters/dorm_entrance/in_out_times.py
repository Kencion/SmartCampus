'''
Created on 2017年11月23日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class in_out_times(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年进出宿舍次数
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select count(*) from dorm_entrance where student_num='" + student_num + "' and DATE_FORMAT(record_time,'%Y')='" + school_year + "'")
            in_out_times = self.executer.fetchone()[0]
            self.executer.execute("update students set in_out_times =%s where student_num=%s" , (in_out_times, student_num + school_year))
        
    @MyLogger.myException
    def rankit(self):
        pass
