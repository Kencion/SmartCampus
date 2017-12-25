'''
Created on 2017年11月29日

@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class Failed_failed_num(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_avg_level')

    @MyLogger.myException
    def calculate(self):
        '''
                            计算failed_failed_num：挂科重修后任然没通过的数目
                            从students表中取出信息，按照students表的学号，再将挂科信息填充到students表中。
        '''
        sql = "select student_num,failed_num,failed_pass_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            failed_failed_num = 0
            if i[1] is not None and i[2] is not None:
                student_num = str(i[0])
                failed_num = int(i[1])
                failed_pass_num = int(i[2])
                failed_failed_num = failed_num - failed_pass_num
                sql = "update students set failed_failed_num = '" + str(failed_failed_num) + "' where student_num = '" + str(student_num) + "'"
                self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
