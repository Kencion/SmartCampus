'''
@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class hornorary_title1(FeatureCalculater.FeatureCalculater):

    @MyLogger.myException
    def calculate(self):
        '''
                计算获得荣誉称号
        '''
        sql = "update students set avg_hornorary_times=0"
        self.executer.execute(sql)
        sql = "select student_num,left(grant_year,4),count(*) from hornorary_handled group by student_num,left(grant_year,4)"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            sql = "update students set avg_hornorary_times=%s where student_num=%s"
            self.executer.execute(sql, (re[2], (re[0] + re[1])))
        
        sql = "update students set hornorary_rank=null"
        self.executer.execute(sql)
        sql = "select student_num,left(grant_year,4),grant_rank from hornorary_handled"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            sql = "update students set hornorary_rank=%s where student_num=%s"
            self.executer.execute(sql, (re[2], (re[0] + re[1])))
        
        sql="update students set hornorary_rank=null"
        self.executer.execute(sql)
        sql="select student_num,left(grant_year,4),grant_rank from hornorary_handled"
        self.executer.execute(sql)
        result=self.executer.fetchall()
        for re in result:
            sql="update students set hornorary_rank=%s where student_num=%s"
            self.executer.execute(sql,(re[2],(re[0]+re[1])))
        
    @MyLogger.myException
    def cluster(self):
        pass
