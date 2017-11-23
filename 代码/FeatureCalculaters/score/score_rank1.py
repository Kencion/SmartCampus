'''
Created on 2017年11月22日

@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class score_rank1(FeatureCalculater.FeatureCalculater):
    '''
            计算成绩排名
    '''
    def setLevel(self):
        pass
    
    def calculate(self):
        sql = "select student_num from students"
        self.executer.execute(sql)
        sql = "select student_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            rank1 = 0
            rank2 = 0
            rank = 0
            stu_num = str(i[0])[:-4]
            school_year = str(i[0])[-4:]
            next_year = str(int(school_year) + 1)
            year1 = school_year + "/" + next_year + "-1"
            year2 = school_year + "/" + next_year + "-2"
            sql = "select Rank from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"  
            #print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            #print(stu1)
            if(stu1 != None):
                rank1 = int(stu1[0])
            sql = "select Rank from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            if(stu2 != None):
                rank2 = float(stu2[0])
            rank = (rank1 + rank2) / 2
            print(rank)
            sql = "update students set score_rank = " + str(rank) + " where student_num = '" + stu_num + school_year + "'"
            self.executer.execute(sql)
            
    @MyLogger.myException
    def rankit(self):
        pass
