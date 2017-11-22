'''
Created on 2017Äê11ÔÂ22ÈÕ

@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class scholarship_amount(FeatureCalculater.FeatureCalculater):
    '''
            è®¡ç®—è·å¾—å¥–å­¦é‡‘çš„é‡‘é¢
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        sql = "select student_num,sum(amount) as amount,grant_year,count(*) as times from hornorary_title where title_name!="" group by student_num,grant_year"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        # print(result)
        for re in result:
            sql = "update students set hornorary_amount=%s,avg_hornorary_times=%s where student_num=%s and school_year=%s"
            # sql="update students set hornorary_amount=%s,avg_hornorary_times=%s where student_num=%s and school_year=%s"
            self.executer.execute(sql, (int(re[1]), int(re[3]), re[0], re[2]))
            # print(re[1])
            # cursor.execute(sql,(re[0],re[1],re[2],re[3],int(count)))
        
    @MyLogger.myException
    def rankit(self):
        pass
