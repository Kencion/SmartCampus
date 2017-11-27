'''
Created on 2017年11月21日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class library_week_study_time(FeatureCalculater.FeatureCalculater):

    @MyLogger.myException
    def calculate(self):
        '''
                        计算每一学年周末图书馆学习时间
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            sql = "SELECT sum(seat_time) FROM library_study_time where student_num =' " + student_num + "' AND DAYOFYEAR(select_seat_time)= " + str(school_year) + " AND DAYOFWEEK(select_seat_time) in (6,7)"
            self.executer.execute(sql)
            library_week_study_time = self.executer.fetchone()[0]
            if library_week_study_time == None:
                library_week_study_time = 0
            sql = "update students set library_week_study_time =" + str(library_week_study_time) + " where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
        
    @MyLogger.myException
    def cluster(self):
        maxx, minn, cent = FeatureCalculater.FeatureCalculater.cluster(self, featureName='library_week_study_time', clusters=4, sql="SELECT library_week_study_time FROM students WHERE library_week_study_time != 0")
        sql = "SELECT max(library_week_study_time) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write("library_week_study_time" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
