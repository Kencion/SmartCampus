'''
Created on 2017年12月19日

@author: yzh
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class canteen_consumption_divide_by_consumption(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='canteen_amount_divide_by_consumption')

    @my_exception_handler
    def calculate(self):
        '''
                            计算食堂消费额占总消费额的比例
        '''
        sql = "select student_num,canteen_total_amount,consumption from students"
        
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
             
            stu_num = i[0]
            
            if i[1] is not None :
                
                canteen_consumption = i[1]
                
                if i[2] is not None:
                    if i[2] != 0:
                        consumption = i[2]
                        res = float(canteen_consumption) / float(consumption)
                    
                        sql = "update students set canteen_amount_divide_by_consumption = " + str(res) + " where student_num = '" + str(stu_num) + "'"
                        self.executer.execute(sql)
                    else:
                        print("总消费额为0，学号是："+stu_num)
                
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
