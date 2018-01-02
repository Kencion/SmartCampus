'''
Created on 2017年11月22日

@author: yzh
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class failed_num1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='failed_num')
    
    @my_exception_handler
    def calculate(self):
        '''
                            计算挂科的数目
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将挂科信息填充到students表中。
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                failed_num1 = 0
                pass_num1 = 0
                failed_num2 = 0
                pass_num2 = 0
                failed_num = 0
                pass_num = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None :
                    failed_num1 = int(stu1[0])
                    pass_num1 = int(str(stu1[1])[:-1])
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"   
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None:
                    failed_num2 = int(stu2[0])
                    pass_num2 = int(str(stu2[1])[:-1])
                    
                failed_num = failed_num1 + failed_num2
                pass_num = pass_num1 + pass_num2
                sql = "update students set failed_num = " + str(failed_num) + " where student_num = '" + stu_num + str(year) + "'"

                t = self.executer.execute(sql)
                if t == 0:
                    self.add_student(stu_num + str(year))
                    self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
