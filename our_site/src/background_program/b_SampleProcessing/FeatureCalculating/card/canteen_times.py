'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
 
class canteen_times(FeatureCalculater):
    
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
                sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '"+ str(year2) +"-08-31' and type = 'canteen'" 
#                 print(sql)
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
#                 print(count)
                sql = "update students set canteen_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
#                 print(sql)
                self.executer.execute(sql)
#             print(stu_num)
#         print("ok")
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.cluster(self,featureName='canteen_times', clusters=4, sql="SELECT canteen_times FROM students WHERE canteen_times is not NULL")
        maxx[len(maxx) - 1] = 100
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "canteen_times字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
# times = canteen_times()
# times.calculate()