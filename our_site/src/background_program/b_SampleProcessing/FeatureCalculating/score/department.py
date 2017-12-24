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
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select department from score where student_num=%s", (student_num))
            department = self.executer.fetchone()[0]
            self.executer.execute("update students set hornorary_rank =%s where student_num=%s" , (department, student_num + school_year))
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
