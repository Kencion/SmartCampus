'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class library_entrance(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_study_time')
    
    @my_exception_handler
    def calculate(self):
        '''
                计算每一学年图书馆进出
        '''
        student_num = str(self.student.getStudentId())
        for school_year in self.school_year:
            sql = "SELECT sum(seat_time) FROM library_study_time where student_num = " + student_num + " AND DAYOFYEAR(select_seat_time)=" + str(school_year)
            self.executer.execute(sql)
            library_study_time = self.executer.fetchone()[0]
            sql = "update students set library_study_time ='" + str(library_study_time) + "' where student_num=" + student_num + " AND school_year =" + str(school_year)
            self.executer.execute(sql)
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

