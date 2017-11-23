'''
@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
from boto.sdb.db.sequence import double

class participation_avg_point1(FeatureCalculater.FeatureCalculater):
    '''
            计算活动持续时间
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        sql="select stu_num,DATE_FORMAT(Start_time, '%Y'),sum(Participation_point)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y')"
        self.executer.execute(sql)
        result=self.executer.fetchall()
        for re in result:
            sql="update students set participation_avg_point=%s where student_num=%s"
            self.executer.execute(sql,(double(re[2]),re[0]+str(int(re[1])-1)))
        
    @MyLogger.myException
    def rankit(self):
        pass
