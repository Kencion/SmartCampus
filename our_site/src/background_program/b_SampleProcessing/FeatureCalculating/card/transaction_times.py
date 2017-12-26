'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class transaction_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='transaction_times')

    @my_exception_handler
    def calculate(self):
        '''
                            计算总消费次数
        '''
#         print("start")
        sql = 'select max(date) from card'
        self.executer.execute(sql)
        lastestItem_date = self.executer.fetchone()[0]
        if lastestItem_date.month < 9:
            lyear = lastestItem_date.year - 1
        else:
            lyear = lastestItem_date.year
            
        sql = "select distinct(student_num) from card"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        
        for i in e:
            stu_num = str(i[0])
            grade = int(stu_num[3:7])
            
            '''
                                    先处理第一年的特殊情况
            '''
            year1 = grade
            year2 = year1 + 1
            sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
#                 print(sql)
            self.executer.execute(sql)
            count = self.executer.fetchone()[0]
#                 print(count)
            if count != 0:
                sql = "update students set transaction_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
#                     print(sql)
                t = self.executer.execute(sql)
                if t == 0:
                    sql = "INSERT INTO students (student_num,transaction_times) VALUES (" + stu_num + str(year1) + "," + str(count) + ")"
                    self.executer.execute(sql)
                    print(sql)
            else:
                print("计算总消费次数这个学生这个学年有问题：" + stu_num + "  " + str(year1))
                
            for year1 in range(grade + 1, lyear):
                year2 = year1 + 1
                sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
#                 print(sql)
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
#                 print(count)
                if count != 0:
                    sql = "update students set transaction_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
#                     print(sql)
                    t = self.executer.execute(sql)
                    if t == 0:
                        sql = "INSERT INTO students (student_num,transaction_times) VALUES (" + stu_num + str(year1) + "," + str(count) + ")"
                        self.executer.execute(sql)
                        print(sql)
                else:
                    print("计算总消费次数这个学生这个学年有问题：" + stu_num + "  " + str(year1))
#             print(stu_num)
#         print("ok")
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

# times = transaction_times()
# times.calculate()
