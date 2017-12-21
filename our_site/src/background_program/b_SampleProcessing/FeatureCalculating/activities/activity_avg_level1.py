'''
@author: yhj
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class activity_avg_level1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_avg_level')
     
    @MyLogger.myException
    def calculate(self):
        '''
                计算活动平均活跃度得分
        '''
        sql = "select Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(Active_level)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            re[1].split('-')
            if int(re[1][6:7]) < 9:
                sql = "update students set activity_avg_level=(activity_avg_level+%s)/2 where student_num=%s"
                self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
            else:
                sql = "update students set activity_avg_level=(activity_avg_level+%s)/2 where student_num=%s "
                self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
