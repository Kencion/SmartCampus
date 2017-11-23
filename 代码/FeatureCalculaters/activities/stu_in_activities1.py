'''
@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
from boto.sdb.db.sequence import double

class stu_in_activities1(FeatureCalculater.FeatureCalculater):
    '''
            计算活动持续时间
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        sql = "update students set activity_last_time=%s"
        self.executer.execute(sql, double(0))
        sql = "select Distinct Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(time_to_sec(timediff(Finish_time,Start_time))) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
#         print(result)
        for re in result:
            re[1].split('-')
            if int(re[1][6:7]) < 9:
                sql = "update students set activity_last_time=%s where student_num=%s"
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                # print(((str)(re[1][0:4])))
            else:
                sql = "update students set activity_last_time=%s where student_num=%s "
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(re[1][0:4])))
                # print((str)(re[1][0:4])+'/'+((str)((int)(re[1][0:4])+1)))
        
    @MyLogger.myException
    def rankit(self):
        pass
