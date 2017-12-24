'''
Created on 2017年12月19日

@author: yzh
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class canteen_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='canteen_times')
     
    @my_exception_handler
    def calculate(self):
        '''
                            计算食堂消费次数
        '''
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            for year1 in range(2014, 2017):
                year2 = year1 + 1
                sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-08-01' and '" + str(year2) + "-07-31' and type = 'canteen'" 
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
                if count != 0:
                    sql = "update students set canteen_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                    self.executer.execute(sql)
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

