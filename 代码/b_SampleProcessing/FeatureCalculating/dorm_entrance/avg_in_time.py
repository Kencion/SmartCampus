'''
@author: yhj
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

class avg_in_time(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        sql="select student_num,avg(max_day_in_time) from dorm_entrance_handled where week_num='6' or week_num='7' group by student_num,DATE_FORMAT(date, '%Y') "
        self.executer.execute(sql)
        result=self.executer.fetchall() 
        for re in result:
            sql="update students set avg_in_time=%s where student_num=%s"
            self.executer.execute(sql,(float(re[1]),re[0]))