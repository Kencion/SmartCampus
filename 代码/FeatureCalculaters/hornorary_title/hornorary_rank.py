'''
Created on 2017年11月23日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class hornorary_rank(FeatureCalculater.FeatureCalculater):
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年内获得荣誉的等级
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            # 一个学生可能会获得很多的荣誉称号
            # 这里先直接搜索到一条就当成是这个
            #
            # 之后会用数值代表这个，比如一个学生获得一次校级（5），一次院级（3），那就5+3=8
            self.executer.execute("select grant_rank from hornorary_handled where student_num=%s and grant_year=%s", (student_num, school_year + "-" + str(int(school_year) + 1)))
            avg_hornorary_times = self.executer.fetchone()[0]
            print(avg_hornorary_times)
            self.executer.execute("update students set hornorary_rank =%s where student_num=%s" , (avg_hornorary_times, student_num + school_year))
        
    @MyLogger.myException
    def rankit(self):
        pass
