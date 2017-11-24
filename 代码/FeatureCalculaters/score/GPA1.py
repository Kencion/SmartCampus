'''
Created on 2017年11月21日

@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class GPA1(FeatureCalculater.FeatureCalculater):
    '''
            计算GPA
    '''
    def setLevel(self):
        pass
    
    def calculate(self):
        sql = "select student_num from students"
        self.executer.execute(sql)
        print(sql)
        e = self.executer.fetchall()
        for i in e:
            GPA1 = 0
            credit1 = 0
            GPA2 = 0
            credit2 = 0
            stu_num = str(i[0])[:-4]
            school_year = str(i[0])[-4:]
            next_year = str(int(school_year) + 1)
            year1 = school_year + "/" + next_year + "-1"
            year2 = school_year + "/" + next_year + "-2"
            sql = "select GPA,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"
            print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            print(stu1)
            if(stu1 is not None):
                GPA1 = float(stu1[0])
                credit1 = int(stu1[1])
            sql = "select GPA,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            if(stu2 is not None):
                GPA2 = float(stu2[0])
                credit2 = int(stu2[1])
            if((credit1 + credit2) != 0):
                GPA = (GPA1 * credit1 + GPA2 * credit2) / (credit1 + credit2)
            print(GPA)
            sql = "update students set GPA = " + str(GPA) + " where student_num = '" + stu_num + school_year + "'"
            self.executer.execute(sql)
            
    @MyLogger.myException
    def rankit(self):
        pass
