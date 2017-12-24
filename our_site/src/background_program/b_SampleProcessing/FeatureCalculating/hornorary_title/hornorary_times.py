'''
Created on 2017年11月23日
 
@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class hornorary_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_avg_level')
         
    @my_exception_handler
    def calculate(self):
        '''
                计算一学年内获得荣誉次数
        '''
        sql = "update students set hornorary_times=0"
        self.executer.execute(sql)
        sql = "select student_num,left(grant_year,4),count(*) from hornorary_handled group by student_num,left(grant_year,4)"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            sql = "update students set hornorary_times=%s where student_num=%s"
            self.executer.execute(sql, (re[2], (re[0] + re[1])))  
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)    
