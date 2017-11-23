'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class scholarship_rank(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算获得奖学金的等级
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            self.executer.execute("SELECT rank FROM scholarship where student_num =%s AND grant_year=%s", (student_num , school_year))
            scholarship_rank = self.executer.fetchone()[0]
            self.executer.execute("update students set scholarship_rank =%s where student_num=", (scholarship_rank, student_num + str(school_year)))
        
    @MyLogger.myException
    def rankit(self):
        pass
