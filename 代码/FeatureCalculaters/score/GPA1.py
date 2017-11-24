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
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
        #     print(str(i[0]))
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade,2017):
                GPA1 = 0
                credit1 = 0
                GPA2 = 0
                credit2 = 0
                GPA = 0
                year1 = str(year)+'/'+str(year+1)+'-1'
                year2 = str(year)+'/'+str(year+1)+'-2'
                sql = "select GPA,course_credit from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"   
        #         print(sql)
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
        #         print(stu1)
                
                if stu1 is not None and stu1[0] is not None:
                    GPA1 = float(stu1[0])
                    credit1 = int(stu1[1])
                sql = "select GPA,course_credit from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"  
        #         print(sql)
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
        #         print(stu2)
                if stu2 is not None and stu2[0] is not None:
                    GPA2 = float(stu2[0])
                    credit2 = int(stu2[1])
                if((credit1+credit2)!=0):
                    GPA = (GPA1*credit1+GPA2*credit2)/(credit1+credit2)
                    sql = "update students set GPA = "+str(GPA)+" where student_num = '"+stu_num+str(year)+"'"
                    self.executer.execute(sql)
#                 else:
#                     print("err!")
#                     print(stu_num)
#         print("ok")
            
    @MyLogger.myException
    def rankit(self):
        pass
gpa = GPA1()
gpa.calculate()