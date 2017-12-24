'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class library_study_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_study_time')
        
    @my_exception_handler
    def calculate(self):
        '''
                        计算每一学年图书馆学习时间
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            sql = "SELECT sum(seat_time),DATE_FORMAT(select_seat_time,'%m') FROM library_study_time where student_num = '" + student_num + "' AND DATE_FORMAT(select_seat_time,'%Y')=" + str(school_year)
            self.executer.execute(sql)
            try:
                result = self.executer.fetchone()
                library_study_time, month = result[0], result[1]
                if int(month) < 9:
                    school_year = int(school_year) - 1
            except:
                library_study_time = 0   
            sql = "update students set library_study_time =" + str(library_study_time) + " where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
         
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

