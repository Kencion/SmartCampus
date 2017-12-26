'''
Created on 2017年11月23日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class department(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='hornorary_rank')

    @my_exception_handler
    def calculate(self):
        '''
                        计算学生的系别
        '''
        sql = "SELECT DISTINCT student_num FROM score"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            for school_year in self.school_year:
                sql = "select department from score where student_num='{0}'".format(student_num)
                self.executer.execute(sql)
                try:
                    department = self.executer.fetchone()[0]
                except:
                    pass
                sql = "update students set hornorary_rank ={0} where student_num='{1}'".format(department, student_num + school_year)
                if self.executer.execute(sql) == 0:
                    self.add_student(student_num + str(school_year))
                    self.executer.execute(sql)
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
