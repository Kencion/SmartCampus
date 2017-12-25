'''
@author: yhj
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class activity_last_time1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_last_time')
        
    @my_exception_handler
    def calculate(self):
        '''
                计算活动持续时间
        '''
        sql = "update students set activity_last_time=%s"
        self.executer.execute(sql, float(0))
        sql = "select Distinct Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(time_to_sec(timediff(Finish_time,Start_time))) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
#         print(result)
        for re in result:
            if re is None:
                pass
            else:
                re[1].split('-')
                if int(re[1][6:7]) < 9:
                    sql = "update students set activity_last_time=activity_last_time+%s where student_num=%s"
                    num=self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                    if num==0:
                        sql = "insert into students(student_num,activity_last_time) values(%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + (str)(int(re[1][0:4]) - 1),float(re[2])))
                else:
                    sql = "update students set activity_last_time=activity_last_time+%s where student_num=%s "
                    self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
                    if num==0:
                        sql = "insert into students(student_num,activity_last_time) values(%s,%s)"
                        self.executer.execute(sql, (str(re[0]) + (str)(int(re[1][0:4])),float(re[2])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)     
