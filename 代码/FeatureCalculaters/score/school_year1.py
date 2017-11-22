'''

'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class school_year1(FeatureCalculater.FeatureCalculater):
    '''
            计算获得奖学金的金额
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        sql = "select DISTINCT stu_num,left(school_year, 9) from score"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        print(result)
        for re in result:
            str(re[1]).split('/')
            sql = "update students set school_year=%s where student_num=%s"
            # print(re[0],re[1],re[2],re[3])
            self.executer.execute(sql, (re[1], str(re[0]) + re[1][0:4]))
            # print(str(re[0])+re[1][0:4])
           # cursor.execute(sql)
        # sql="update students set activity_last_time=%s where student_num=%s and school_year=%s"
        
    @MyLogger.myException
    def rankit(self):
        pass