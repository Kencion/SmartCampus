'''
@author: yhj
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from ..FeatureCalculater import FeatureCalculater


class school_year1(FeatureCalculater):
    
    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='school_year')

    @my_exception_handler
    def calculate(self):
        '''
                计算获得奖学金的金额
        '''
        sql = "select DISTINCT stu_num,left(school_year, 9) from score"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        print(result)
        for re in result:
            str(re[1]).split('/')
            sql = "update students set school_year=%s where student_num=%s"
            self.executer.execute(sql, (re[1], str(re[0]) + re[1][0:4]))
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
