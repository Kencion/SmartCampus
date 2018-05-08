from background_program.z_Tools.my_exceptions import my_exception_handler
from .FeatureCalculater import FeatureCalculater


class activity_avg_level1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_avg_level')
     
    @my_exception_handler
    def calculate(self):
        '''
                计算活动平均活跃度得分
        '''
        sql = "update students set activity_avg_level=%s"
        self.executer.execute(sql, float(0))
        sql = "select Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(Active_level)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            if re is None:
                pass
            else:
                re[1].split('-')
                if int(re[1][5:7]) < 9:
                    sql = "update students set activity_avg_level=(activity_avg_level+%s)/2 where student_num=%s"
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4]) - 1))
                        sql2 = "update students set activity_avg_level=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                else:
                    sql = "update students set activity_avg_level=(activity_avg_level+%s)/2 where student_num=%s "
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + str(re[1][0:4])))
                    if num == 0:
                        self.add_student(str(re[0]) + str(re[1][0:4]))
                        sql2 = "update students set activity_avg_level=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0), str(re[0]) + (str)(int(re[1][0:4]))))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + str(re[1][0:4])))
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=2)

        
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
                if int(re[1][5:7]) < 9:
                    sql = "update students set activity_last_time=activity_last_time+%s where student_num=%s"
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4]) - 1))
                        sql2 = "update students set activity_last_time=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                else:
                    sql = "update students set activity_last_time=activity_last_time+%s where student_num=%s "
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4])))
                        sql2 = "update students set activity_last_time=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0), str(re[0]) + (str)(int(re[1][0:4]))))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=2)     

        
class activity_num1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_last_time')
        
    @my_exception_handler
    def calculate(self):
        '''
                计算每学年参与活动数量
        '''
        sql = "update students set activity_num=%s"
        self.executer.execute(sql, float(0))
        sql = "select Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            if re is None:
                pass
            else:
                re[1].split('-')
                if int(re[1][5:7]) < 9:
                    sql = "update students set activity_num=activity_num+%s where student_num=%s"
                    num = self.executer.execute(sql, (int(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4]) - 1))
                        sql2 = "update students set activity_num=%s where student_num=%s"
                        self.executer.execute(sql2, (int(0), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                        self.executer.execute(sql, (int(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                else:
                    sql = "update students set activity_num=activity_num+%s where student_num=%s "
                    num = self.executer.execute(sql, (int(0), str(re[0]) + (str)(re[1][0:4])))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(re[1][0:4]))
                        sql2 = "update students set activity_num=%s where student_num=%s"
                        self.executer.execute(sql2, (int(re[2]), str(re[0]) + (str)(int(re[1][0:4]))))
                        self.executer.execute(sql, (int(re[2]), str(re[0]) + (str)(re[1][0:4])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=2)  

        
class participation_avg_point1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='participation_avg_point')
    
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
                        self.executer.execute(sql2, (float(0), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                else:
                    sql = "update students set participation_avg_point=(participation_avg_point+%s)/2 where student_num=%s "
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4])))
                        sql2 = "update students set participation_avg_point=%s where student_num=%s"
                        self.executer.execute(sql2, (float(0), str(re[0]) + (str)(int(re[1][0:4]))))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4) 
