'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class scholarship_amount(FeatureCalculater.FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                        计算获得奖学金的金额
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT amount FROM scholarship where student_num = '" + student_num + "' AND grant_year=" + str(school_year)
            self.executer.execute(sql)
            scholarship_amount = self.executer.fetchone()[0]
            if scholarship_amount == None:
                scholarship_amount = 0
            sql = "update students set scholarship_amount =" + str(scholarship_amount) + " where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='scholarship_amount', clusters=4, sql="SELECT scholarship_amount FROM students WHERE scholarship_amount != 0")
        sql = "SELECT max(scholarship_amount) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"FeatureCalculaters/聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write( "scholarship_amount" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
