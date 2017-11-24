'''
Created on 2017年11月22日

@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class failed_num1(FeatureCalculater.FeatureCalculater):
    def calculate(self):
        '''
                计算挂科数目
        '''
        sql = "select student_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            num1 = 0
            num2 = 0
            stu_num = str(i[0])[:-4]
            school_year = str(i[0])[-4:]
            next_year = str(int(school_year) + 1)
            year1 = school_year + "/" + next_year + "-1"
            year2 = school_year + "/" + next_year + "-2"
            sql = "select substring_index(failed_num,'(',1) from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"
            print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            print(stu1)
            if(stu1 is not None):
                num1 = float(stu1[0])
            sql = "select substring_index(failed_num,'(',1) from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            if(stu2 is not None):
                num2 = float(stu2[0])
            num = num1 + num2
            print(num)
            sql = "update students set failed_num = " + str(num) + " where student_num = '" + stu_num + school_year + "'"
            self.executer.execute(sql)
            
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='failed_num', clusters=4, sql="SELECT failed_num FROM students WHERE failed_num != 0")
        sql = "SELECT max(failed_num) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"FeatureCalculaters/聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write( "failed_num" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()