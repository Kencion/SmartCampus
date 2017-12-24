'''
Created on 2017年11月22日

@author: yzh
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class score_rank1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='score_rank')
    
    @my_exception_handler
    def calculate(self):
        '''
                    计算成绩排名
                    从score表中取出信息，按照score表中的学号索取到students表的学号，再将成绩排名信息填充到students表中。
        rank = (rank1+rank2)/2 取算术平均
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                rank1 = 0
                rank2 = 0
                rank = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select rank from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None :
                    rank1 = int(stu1[0])
                    
                sql = "select rank from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"   
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None:
                    rank2 = int(stu2[0])
                    
                if stu1 is not None and stu2 is not None: 
                    rank = int((rank1 + rank2) / 2)
                    sql = "update students set score_rank = " + str(rank) + " where student_num = '" + stu_num + str(year) + "'"
                    self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
