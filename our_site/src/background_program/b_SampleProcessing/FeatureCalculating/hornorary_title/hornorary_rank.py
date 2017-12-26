'''
Created on 2017年11月23日

@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class hornorary_rank(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='hornorary_rank')
        
    @my_exception_handler
    def calculate(self):
        '''
                计算一学年内获得荣誉的等级
    # 一个学生可能会获得很多的荣誉称号
    # 这里先直接搜索到一条就当成是这个
    #
    # 之后会用数值代表这个，比如一个学生获得一次校级（5），一次院级（3），那就5+3=8
        '''
        sql = "select student_num,left(grant_year,4),grant_rank from hornorary_handled"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            hornorary_rank = 0
            if re[2] == '校级':
                hornorary_rank += 5
            elif re[2] == '院级':
                hornorary_rank += 3
            sql = "update students set hornorary_rank=hornorary_rank+%s where student_num=%s"
            self.executer.execute(sql, (int(hornorary_rank), (re[0] + re[1])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
