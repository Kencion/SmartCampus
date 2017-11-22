'''
Created on 2017骞�11鏈�21鏃�
 
@author: 95679
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
 
class score1(FeatureCalculater.FeatureCalculater):
    def calculate(self):
        #yzh
        sql = "select student_num,school_year from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            school_year = str(i[1])
            next_year = str(int(str(i[1])) + 1)
            year1 = school_year + "/" + next_year + "-1"
            year2 = school_year + "/" + next_year + "-2"
            sql = "select score,course_credit from score where stu_num = " + stu_num + " and school_year = " + year1   
            print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            print(stu1)
            score1 = float(stu1[0])
            credit1 = int(stu1[1])
            sql = "select score,course_credit from score where stu_num = " + stu_num + " and school_year = " + year2
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            score2 = float(stu2[0])
            credit2 = int(stu2[1])
            score = (score1 * credit1 + score2 * credit2) / (credit1 + credit2)
            print(score)
            self.executer.execute("update students set score = " + score + " where student_num = " + stu_num + " and school = " + school_year)
        print("ok")
        #yhj
        #score表：导入字段 学年
        sql = "select DISTINCT stu_num,left(school_year, 9) from score"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        print(result)
        for re in result:
            str(re[1]).split('/')
            sql = "update students set school_year=%s where student_num=%s"
            # print(re[0],re[1],re[2],re[3])
            self.executer.execute(sql, (re[1], str(re[0]) + re[1][0:4]))
            # print(str(re[0])+re[1][0:4])
            # cursor.execute(sql)
        # sql="update students set activity_last_time=%s where student_num=%s and school_year=%s"
