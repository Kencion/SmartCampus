'''
Created on 2017年11月21日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class scholarship_rank(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='scholarship_rank')
        
    @my_exception_handler
    def calculate(self):
        '''
                计算获得奖学金的等级
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT scholarship_type FROM scholarship_handled where student_num ='{0}' AND left(grant_year,4)='{1}'".format(str(student_num) , str(school_year))
            self.executer.execute(sql)
            try: 
                scholarship_ranks = self.executer.fetchall()
                scholarship_rank = 0
                for i in scholarship_ranks:
                    if i[0] == '国家奖学金':
                        scholarship_rank += 19
                    elif i[0] == '本科生优秀学生奖学金':
                        scholarship_rank += 17
                    elif i[0] == '校级奖学金':
                        scholarship_rank += 15
                    elif i[0] == '国家励志奖学金':
                        scholarship_rank += 13
                    elif i[0] == '奖学金':
                        scholarship_rank += 11
                    elif i[0] == '其他来源奖学金':
                        scholarship_rank += 9
                    elif i[0] == '-三大奖校级奖学金':
                        scholarship_rank += 7
            except:
                scholarship_rank = 0
            sql = "update students set scholarship_rank ='{0}' where student_num='{1}'".format(scholarship_rank, student_num + str(school_year))
            self.executer.execute(sql)

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
