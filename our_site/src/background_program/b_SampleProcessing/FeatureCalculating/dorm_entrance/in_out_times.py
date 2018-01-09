'''
Created on 2017年11月23日
@author: Jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class in_out_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='in_out_times')

    @my_exception_handler
    def calculate(self):
        '''
                计算一学年进出宿舍次数
        '''
        sql = "SELECT DISTINCT student_num FROM dorm_entrance"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year=self.get_school_year(student_num)
            for school_year in self.school_year:
                self.executer.execute("select count(*),DATE_FORMAT(record_time,'%m') from dorm_entrance where student_num='{0}' and DATE_FORMAT(record_time,'%Y')='{1}'".format(student_num, school_year))
                try:
                    result = self.executer.fetchone()
                    in_out_times, month = result[0], result[1]
                    if int(month) < 9:
                        school_year = int(school_year) - 1
                except:
                    continue
                sql = "update students set in_out_times ={0} where student_num='{1}'" .format (int(in_out_times), student_num + str(school_year))
                if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
