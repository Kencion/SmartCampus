'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class scholarship_rank(FeatureCalculater.FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算获得奖学金的等级
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            self.executer.execute("SELECT rank FROM scholarship where student_num =%s AND grant_year=%s", (student_num , school_year))
            scholarship_rank = self.executer.fetchone()[0]
            self.executer.execute("update students set scholarship_rank =%s where student_num=", (scholarship_rank, student_num + str(school_year)))
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='scholarship_rank', clusters=4, sql="SELECT scholarship_rank FROM students WHERE scholarship_rank != 0")
        sql = "SELECT max(scholarship_rank) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write( "scholarship_rank" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
