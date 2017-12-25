'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class library_week_study_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_week_study_time')

    @my_exception_handler
    def calculate(self):
        '''
                        计算每一学年周末图书馆学习时间
        '''
        sql = "SELECT DISTINCT student_num FROM library_study_time"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            for school_year in self.school_year:
                sql = "SELECT sum(seat_time),DATE_FORMAT(select_seat_time,'%m') FROM library_study_time where student_num ='{0}' AND DATE_FORMAT(select_seat_time,'%Y')='{1}' AND DAYOFWEEK(select_seat_time) in (6,7)".format(student_num, str(school_year))
                self.executer.execute(sql)
                result = self.executer.fetchone()
                library_week_study_time, month = result[0], result[1]
                if library_week_study_time is not None:
                    sql = "update students set library_week_study_time =" + str(library_week_study_time) + " where student_num='" + student_num + str(school_year) + "'"
                    if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
