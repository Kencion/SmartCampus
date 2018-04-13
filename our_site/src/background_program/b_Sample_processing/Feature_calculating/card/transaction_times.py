'''
Created on 2017年12月19日

@author: yzh
'''
from background_program.z_Tools.my_exceptions import my_exception_handler
#from ..FeatureCalculater import FeatureCalculater
from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
 
class transaction_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='transaction_times')
    @my_exception_handler
    def calculate(self):
        sql="SELECT student_num,DATE_FORMAT(date, '%Y-%m'),count(*) from card group by student_num,DATE_FORMAT(date, '%Y-%m') order by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        print(result)
        student_num = result[0][0]
        month_tag = 0
        month_flag=0
        year_tag = result[0][0][3:7]
        count=0
        for re in result:
            re[1].split('-')
            month = int(re[1][5:7])
            year2 = int(re[1][0:4])
            if re[0] != student_num:
                if int(re[0][3:7])==year2 and month<9:
                    month_tag=1
                else:
                    month_tag=0
                sql="update students set transaction_times=%s where student_num=%s"
                num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
                student_num=re[0]
                year_tag=re[0][3:7]
                count=0
            #入学第一学年在9月之前有数据的学生，将9月之前的数据归到第一学年
            if year2!=int(year_tag) and month_tag==1 and month<9:
                count+=int(re[2])
            elif month_tag==1 and month>=9 and year2!=int(year_tag):
                sql="update students set transaction_times=%s where student_num=%s"
                num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
                year_tag=year2
                count=0
                count+=int(re[2])
                month_tag=0
            elif year2==int(year_tag) and month_tag==1:
                count+=int(re[2])
                
                
            #入学第一学年在9月之后有数据的学生,第二学年开始都是跑这个部分
            elif month_tag==0 and month>=9 and year2==int(year_tag):
                count+=int(re[2])
            elif month_tag==0 and month<9 and year2!=int(year_tag):
                count+=int(re[2])
            elif month_tag==0 and month<9 and year2>int(year_tag)+1:
                sql="update students set transaction_times=%s where student_num=%s"
                num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
                count=0
                count+=int(re[2])
                year_tag=year2-1
                month_tag=0
            elif month_tag==0 and month>=9 and year2!=int(year_tag):
                if count!=0:
                    sql="update students set transaction_times=%s where student_num=%s"
                    num=self.executer.execute(sql, (float(count), str(student_num)+str(year_tag)))
                count=0
                count+=int(re[2])
                year_tag=year2
                month_tag=0
#     @my_exception_handler
#     def calculate(self):
#         '''
#                             计算总消费次数
#         '''
# #         print("start")
#         sql = 'select max(date) from card'
#         self.executer.execute(sql)
#         lastestItem_date = self.executer.fetchone()[0]
#         if lastestItem_date.month < 9:
#             lyear = lastestItem_date.year - 1
#         else:
#             lyear = lastestItem_date.year
#             
#         sql = "select distinct(student_num) from card"
#         self.executer.execute(sql)
#         e = self.executer.fetchall()
#         
#         for i in e:
#             stu_num = str(i[0])
#             grade = int(stu_num[3:7])
#             
#             '''
#                                     先处理第一年的特殊情况
#             '''
#             year1 = grade
#             year2 = year1 + 1
#             sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
# #                 print(sql)
#             self.executer.execute(sql)
#             count = self.executer.fetchone()[0]
# #                 print(count)
#             if count != 0:
#                 sql = "update students set transaction_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
# #                     print(sql)
#                 t = self.executer.execute(sql)
#                 if t == 0:
#                     sql = "INSERT INTO students (student_num,transaction_times) VALUES (" + stu_num + str(year1) + "," + str(count) + ")"
#                     self.executer.execute(sql)
#                     print(sql)
#             else:
#                 print("计算总消费次数这个学生这个学年有问题：" + stu_num + "  " + str(year1))
#                 
#             for year1 in range(grade + 1, lyear + 1):
#                 year2 = year1 + 1
#                 sql = "select count(transaction_amount) from card where student_num = '" + str(stu_num) + "' and date between '" + str(year1) + "-09-01' and '" + str(year2) + "-08-31' and transaction_amount<0" 
# #                 print(sql)
#                 self.executer.execute(sql)
#                 count = self.executer.fetchone()[0]
# #                 print(count)
#                 if count != 0:
#                     sql = "update students set transaction_times = " + str(count) + " where student_num = '" + stu_num + str(year1) + "'"
# #                     print(sql)
#                     t = self.executer.execute(sql)
#                     if t == 0:
#                         self.add_student(stu_num + str(year1))
#                         self.executer.execute(sql)
# #                         print(sql)
#                 else:
#                     print("计算总消费次数这个学生这个学年有问题：" + stu_num + "  " + str(year1))
# #             print(stu_num)
# #         print("ok")
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

# times = transaction_times()
# times.calculate()
if __name__=='__main__':
    tt=transaction_times()
    tt.calculate()