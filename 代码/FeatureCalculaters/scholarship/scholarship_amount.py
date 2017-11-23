'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class scholarship_amount(FeatureCalculater.FeatureCalculater):
    '''
            计算获得奖学金的金额
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT amount FROM scholarship where student_num = '" + student_num + "' AND grant_year=" + str(school_year)
            self.executer.execute(sql)
            scholarship_amount = self.executer.fetchone()[0]
            if scholarship_amount == None:
                scholarship_amount = 0
            sql = "update students set scholarship_amount =" + str(scholarship_amount) + " where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
        
    @MyLogger.myException
    def rankit(self):
        pass
