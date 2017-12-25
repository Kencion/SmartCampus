'''
Created on 2017年12月19日

@author: yzh
'''

from background_program.z_Tools.my_exceptions import my_exception_handler
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class Consumption(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='Consumption')

    @my_exception_handler
    def calculate(self):
        '''
                            计算总消费额
        '''
        
        sql = 'select max(date) from card'
        self.executer.execute(sql)
        lastestItem_date = self.executer.fetchone()[0]
        if lastestItem_date.month < 9:
            lyear = lastestItem_date.year -1
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
            sql = "select sum(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-07-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
            self.executer.execute(sql)
            count = self.executer.fetchone()[0]
            if count is not None:
                sql = "update students set Consumption = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                t = self.executer.execute(sql)
                if t == 0:
                    sql = "INSERT INTO students (student_num,Consumption) VALUES (" + stu_num + str(year1) +","+str(count)+")"
                    self.executer.execute(sql)
                    print(sql)
            else:
                print("计算总消费额这个学生这个学年有问题："+stu_num+"  "+str(year1))
                    
            for year1 in range(grade+1, lyear):
                year2 = year1 + 1
                sql = "select sum(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
                self.executer.execute(sql)
                count = self.executer.fetchone()[0]
                if count is not None:
                    sql = "update students set Consumption = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
                    t = self.executer.execute(sql)
                    if t == 0:
                        sql = "INSERT INTO students (student_num,Consumption) VALUES (" + stu_num + str(year1) +","+str(count)+")"
                        self.executer.execute(sql)
                        print(sql)
                else:
                    print("计算总消费额这个学生这个学年有问题："+stu_num+"  "+str(year1))
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

