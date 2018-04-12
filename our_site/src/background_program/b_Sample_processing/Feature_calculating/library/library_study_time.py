'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
#from ..FeatureCalculater import FeatureCalculater
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater

class library_study_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_study_time')
        
    @my_exception_handler
    def calculate(self):
        '''
                        计算每一学年图书馆学习时间
        '''
        sql = "update students set library_study_time=%s"
        self.executer.execute(sql, float(0))
        sql = "SELECT DISTINCT student_num FROM library_study_time"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year=self.get_school_year(student_num)
            for school_year in self.school_year:
                sql = "SELECT sum(seat_time),DATE_FORMAT(select_seat_time,'%m') FROM library_study_time where student_num = '" + student_num + "' AND DATE_FORMAT(select_seat_time,'%Y')=" + str(school_year)
                self.executer.execute(sql)
                try:
                    result = self.executer.fetchone()
                    library_study_time, month = result[0], result[1]
                    if int(month) < 9:
                        school_year = int(school_year) - 1
                    sql = "update students set library_study_time =" + str(library_study_time) + " where student_num='" + student_num + str(school_year) + "'"
                    if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)
                except:
                    pass   
         
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

