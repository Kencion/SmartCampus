'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class subsidy_amount(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='subsidy_amount')
        
    @my_exception_handler
    def calculate(self):
        '''
                        计算获得奖学金的金额
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT amount FROM subsidy_handled where student_num = '{0}' AND grant_year='{1}'".format(student_num, school_year)
            self.executer.execute(sql)
            try:
                subsidy_amount = self.executer.fetchone()[0]
            except:
                subsidy_amount = 0
            sql = "update students set subsidy_amount ='{0}' where student_num='{1}'".format(str(subsidy_amount), student_num + school_year)
            self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
