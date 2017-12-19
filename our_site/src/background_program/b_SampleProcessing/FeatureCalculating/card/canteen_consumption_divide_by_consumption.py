'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
 
class canteen_amount_divide_by_consumption(FeatureCalculater):
    
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
                    consumption = i[2]
                    res = float(canteen_consumption)/float(consumption)
                
                    sql = "update students set canteen_amount_divide_by_consumption = " + str(res) + " where student_num = '"+str(stu_num)+"'"
#                     print(sql)
                    self.executer.execute(sql)
                    
                else:
                    print("consumption is 0!!!the student_num = "+str(stu_num))

            else:
                print("canteen_consumption is 0!!!the student_num = "+str(stu_num))
                
#             print(stu_num)    
                
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.cluster(self,featureName='canteen_amount_divide_by_consumption', clusters=4, sql="SELECT canteen_consumption_divide_by_consumption FROM students WHERE canteen_consumption_divide_by_consumption is not NULL")
        maxx[len(maxx) - 1] = 100
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "canteen_amount_divide_by_consumption字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
# times = canteen_amount_divide_by_consumption()
# times.calculate()