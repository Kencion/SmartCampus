'''
@author: yhj
'''
from background_program.z_Tools.my_exceptions import my_exception_handler
from ..FeatureCalculater import FeatureCalculater


class avg_in_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='avg_in_time')
        
    @my_exception_handler
    def calculate(self):
        sql = "select student_num,avg(max_day_in_time) from dorm_entrance_handled where week_num='6' or week_num='7' group by student_num "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            if re is None:
                pass
            else:
                sql = "update students set avg_in_time=%s where student_num=%s"
                num = self.executer.execute(sql, (float(re[1]), re[0]))
                if num == 0:
                    self.add_student(re[0])
                    self.executer.execute(sql, (float(re[1]), re[0]))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
