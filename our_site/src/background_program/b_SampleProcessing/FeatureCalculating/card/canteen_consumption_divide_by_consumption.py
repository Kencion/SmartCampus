'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
 
class canteen_amount_divide_by_consumption(FeatureCalculater):
    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='canteen_amount_divide_by_consumption')
    @MyLogger.myException
    def calculate(self):
        '''
                            计算食堂消费额占总消费额的比例
        '''
#         print("start")
        sql = "select student_num,canteen_total_amount,consumption from students"
        
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
             
            stu_num = i[0]
            
            if i[1] != 0:
                
                canteen_consumption = i[1]
                
                if i[2] != 0:
                    consumption = -1*i[2]
                    res = float(canteen_consumption)/float(consumption)
                
                    sql = "update students set canteen_amount_divide_by_consumption = " + str(res) + " where student_num = '"+str(stu_num)+"'"
#                     print(sql)
                    self.executer.execute(sql)
#             print(stu_num)    
#         print("ok")
                
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
# times = canteen_amount_divide_by_consumption()
# times.calculate()