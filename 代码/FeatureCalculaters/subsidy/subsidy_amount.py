'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class subsidy_amount(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                        计算获得奖学金的金额
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT amount FROM subsidy where student_num = '" + student_num + "' AND grant_year=" + str(school_year)
            self.executer.execute(sql)
            subsidy_amount = self.executer.fetchone()[0]
            sql = "update students set subsidy_amount ='" + str(subsidy_amount) + "' where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
        
    @MyLogger.myException
    def rankit(self):
        pass
