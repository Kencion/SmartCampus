'''
 
@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
 
class score1(FeatureCalculater.FeatureCalculater):
    def calculate(self):
<<<<<<< HEAD
        #yzh
        sql = "select student_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            score1 = 0
            credit1 = 0
            score2 = 0
            credit2 = 0
            score = 0
            #print(str(i[0]))
            stu_num = str(i[0])[:-4]
            school_year = str(i[0])[-4:]
            next_year = str(int(school_year)+1)
            year1 = school_year + "/" +next_year+"-1"
            year2 = school_year + "/" +next_year+"-2"
            
            sql = "select score,course_credit from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"   
        
            #print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            #print(stu1)
            if(stu1!=None):
                #!!!!!!! something wrong
                score1 = float(stu1[0])
                credit1 = int(stu1[1])
            
            sql = "select score,course_credit from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"
            
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            if(stu2!=None):
                score2 = float(stu2[0])
                credit2 = int(stu2[1])
            if((credit1+credit2)!=0):
                score = (score1*credit1+score2*credit2)/(credit1+credit2)
            #print(score)
            sql = "update students set score = "+str(score)+" where student_num = '"+stu_num+school_year+"'"
            #print(sql)
            self.executer.execute(sql)
        #yhj
        #score表：导入字段 学年
=======
        # yzh
        sql = "select student_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            score1 = 0
            credit1 = 0
            score2 = 0
            credit2 = 0
            score = 0
            # print(str(i[0]))
            stu_num = str(i[0])[:-4]
            school_year = str(i[0])[-4:]
            next_year = str(int(school_year) + 1)
            year1 = school_year + "/" + next_year + "-1"
            year2 = school_year + "/" + next_year + "-2"
            
            sql = "select score,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
        
            # print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            # print(stu1)
            if(stu1 is not None):
                score1 = float(stu1[0])
                credit1 = int(stu1[1])
            
            sql = "select score,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"
            
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            if(stu2 is not None):
                score2 = float(stu2[0])
                credit2 = int(stu2[1])
            if((credit1 + credit2) != 0):
                score = (score1 * credit1 + score2 * credit2) / (credit1 + credit2)
            # print(score)
            sql = "update students set score = " + str(score) + " where student_num = '" + stu_num + school_year + "'"
            # print(sql)
            self.executer.execute(sql)
        # yhj
        # score表：导入字段 学年
>>>>>>> 58c8ae438e75386c56a43e66d73b1425c289dc46
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
