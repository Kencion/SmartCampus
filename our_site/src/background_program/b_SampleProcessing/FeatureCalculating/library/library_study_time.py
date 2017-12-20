'''
Created on 2017年11月21日

@author: jack
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class library_study_time(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                        计算每一学年图书馆学习时间
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            sql = "SELECT sum(seat_time),DATE_FORMAT(select_seat_time,'%m') FROM library_study_time where student_num = '" + student_num + "' AND DATE_FORMAT(select_seat_time,'%Y')=" + str(school_year)
            self.executer.execute(sql)
            try:
                result = self.executer.fetchone()
                library_study_time, month = result[0], result[1]
                if int(month) < 9:
                    school_year = int(school_year) - 1
            except:
                library_study_time = 0   
            sql = "update students set library_study_time =" + str(library_study_time) + " where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
         
    @MyLogger.myException
    def cluster(self):
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='library_study_time', clusters=4, sql="SELECT library_study_time FROM students WHERE library_study_time != 0")
        sql = "SELECT max(library_study_time) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
         
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("library_study_time" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
