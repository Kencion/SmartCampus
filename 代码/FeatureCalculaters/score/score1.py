'''
 
@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
 
class score1(FeatureCalculater.FeatureCalculater):
    
    def calculate(self):
        # yzh
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
        #     print(str(i[0]))
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                score1 = 0
                credit1 = 0
                score2 = 0
                credit2 = 0
                score = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select score,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
        #         print(sql)
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
        #         print(stu1)
                
                if stu1 is not None and stu1[0] is not None:
                    score1 = float(stu1[0])
                    credit1 = int(stu1[1])
                sql = "select score,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"  
        #         print(sql)
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
        #         print(stu2)
                if stu2 is not None and stu2[0] is not None:
                    score2 = float(stu2[0])
                    credit2 = int(stu2[1])
                if((credit1 + credit2) != 0):
                    score = (score1 * credit1 + score2 * credit2) / (credit1 + credit2)
                    sql = "update students set score = " + str(score) + " where student_num = '" + stu_num + str(year) + "'"
                    self.executer.execute(sql)
#                 else:
#                     print("err!")
#                     print(stu_num)
        
        # yhj
        # score表：导入字段 学年
#         sql = "select DISTINCT stu_num,left(school_year, 9) from score"
#         self.executer.execute(sql)
#         result = self.executer.fetchall()
#         print(result)
#         for re in result:
#             str(re[1]).split('/')
#             sql = "update students set school_year=%s where student_num=%s"
#             # print(re[0],re[1],re[2],re[3])
#             self.executer.execute(sql, (re[1], str(re[0]) + re[1][0:4]))
            # print(str(re[0])+re[1][0:4])
            # cursor.execute(sql)
        # sql="update students set activity_last_time=%s where student_num=%s and school_year=%s"
    @MyLogger.myException
    def rankit(self):
        pass
