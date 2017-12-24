'''
@author: yhj
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class avg_stay_out_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='avg_stay_out_time')

    @MyLogger.myException
    def calculate(self):
        sql = "select student_num,avg(max_day_in_time-min_day_out_time) from dorm_entrance_handled where week_num!='6' and week_num!='7' group by student_num,DATE_FORMAT(date, '%Y') "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set avg_stay_out_time=%s where student_num=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
