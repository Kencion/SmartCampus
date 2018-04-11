'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
#from ..FeatureCalculater import FeatureCalculater
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater

class subsidy_rank(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='subsidy_rank')
        
    @my_exception_handler
    def calculate(self):
        '''
                        计算获得助学金的等级
        '''
         # 用数值代表这个，一等（5），二等（3），三等（2），不分等（2）
        sql = "update students set subsidy_rank=%s"
        self.executer.execute(sql, float(0))
        sql="select student_num,left(grant_year,4),rank from subsidy_handled "
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            subsidy_rank = 0
            if re[2] == '一等':
                subsidy_rank += 5
            elif re[2] == '二等':
                subsidy_rank += 3
            elif re[2] == '三等':
                subsidy_rank += 2
            elif re[2] == '不分等':
                subsidy_rank += 2
            sql = "update students set subsidy_rank=subsidy_rank+%s where student_num=%s"
            self.executer.execute(sql, (int(subsidy_rank), (re[0] + re[1])))
#         sql = "SELECT DISTINCT student_num FROM subsidy_handled"
#         self.executer.execute(sql)
#         student_nums = [str(i[0]) for i in self.executer.fetchall()]
#         for student_num in student_nums:
#             self.school_year=self.get_school_year(student_num)  
#               
#             for school_year in self.school_year:
#                 try:
#                     sql = "SELECT rank FROM subsidy_handled where student_num = '{0}' AND grant_year='{1}'".format(student_num , school_year)
#                     self.executer.execute(sql)
#                     subsidy_rank = self.executer.fetchone()[0]
#                     sql = "update students set subsidy_rank ='" + str(subsidy_rank) + "' where student_num='" + student_num + str(school_year) + "'"
#                     if self.executer.execute(sql) == 0:
#                             self.add_student(student_num + str(school_year))
#                             self.executer.execute(sql)
#                 except:
#                     pass
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
if __name__=="__main__":
    hr=subsidy_rank()
    hr.calculate()