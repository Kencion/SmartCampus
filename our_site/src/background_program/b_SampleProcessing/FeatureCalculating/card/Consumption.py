'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
 
class Consumption(FeatureCalculater):
    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='Consumption')
    @MyLogger.myException
    def calculate(self):
        '''
                            计算总消费额
        '''
#         print("start")
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            for year1 in range(2014, 2017):
                year2 = year1+1
                sql = "select sum(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-08-01' and '"+ str(year2) +"-07-31' and transaction_amount<0" 
#                 print(sql)
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
                if count is not None:
#                     print(count)
                    sql = "update students set Consumption = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
#                     print(sql)
                    self.executer.execute(sql)
#             print(stu_num)
#         print("ok")
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

# times = Consumption()
# times.calculate()