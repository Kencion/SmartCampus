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
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> parent of f819a9d... 2017.11.24
=======
>>>>>>> parent of f819a9d... 2017.11.24
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
<<<<<<< HEAD
<<<<<<< HEAD
            if(stu1 is not None):
=======
            if(stu1 != None):
>>>>>>> parent of f819a9d... 2017.11.24
=======
            if(stu1 != None):
>>>>>>> parent of f819a9d... 2017.11.24
                GPA1 = float(stu1[0])
                credit1 = int(stu1[1])
            sql = "select GPA,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
<<<<<<< HEAD
<<<<<<< HEAD
            if(stu2 is not None):
=======
            if(stu2 != None):
>>>>>>> parent of f819a9d... 2017.11.24
=======
            if(stu2 != None):
>>>>>>> parent of f819a9d... 2017.11.24
                GPA2 = float(stu2[0])
                credit2 = int(stu2[1])
            if((credit1 + credit2) != 0):
                GPA = (GPA1 * credit1 + GPA2 * credit2) / (credit1 + credit2)
            print(GPA)
            sql = "update students set GPA = " + str(GPA) + " where student_num = '" + stu_num + school_year + "'"
            self.executer.execute(sql)
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 58c8ae438e75386c56a43e66d73b1425c289dc46
=======
>>>>>>> parent of f819a9d... 2017.11.24
=======
>>>>>>> parent of f819a9d... 2017.11.24
            
    @MyLogger.myException
    def rankit(self):
        pass
