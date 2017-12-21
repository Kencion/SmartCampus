'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
 
class canteen_times(FeatureCalculater):
    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='canteen_times')
     
    @MyLogger.myException
    def calculate(self):
        '''
                            计算食堂消费次数
        '''
#         print("start")
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            for year1 in range(2014, 2017):
                year2 = year1+1
                sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-08-01' and '"+ str(year2) +"-07-31' and type = 'canteen'" 
#                 print(sql)
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
#                 print(count)
                if count != 0:
                    sql = "update students set canteen_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
#                     print(sql)
                    self.executer.execute(sql)
#             print(stu_num)
#         print("ok")
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

# times = canteen_times()
# times.calculate()