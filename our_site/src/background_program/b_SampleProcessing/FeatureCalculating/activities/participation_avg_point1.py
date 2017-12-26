'''
@author: yhj
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class participation_avg_point1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_avg_level')
    
    @my_exception_handler
    def calculate(self):
        '''
                计算活动参与平均分
        '''
        sql = "update students set participation_avg_point=%s"
        self.executer.execute(sql, float(0))
        sql = "select Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(Participation_point)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            if re is None:
                pass
            else:
                re[1].split('-')
                if int(re[1][5:7]) < 9:
                    sql = "update students set participation_avg_point=(participation_avg_point+%s)/2 where student_num=%s"
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4]) - 1))
                        sql2 = "update students set participation_avg_point=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0),str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                else:
                    sql = "update students set participation_avg_point=(participation_avg_point+%s)/2 where student_num=%s "
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4])))
                        sql2 = "update students set participation_avg_point=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0),str(re[0]) + (str)(int(re[1][0:4]))))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4) 
