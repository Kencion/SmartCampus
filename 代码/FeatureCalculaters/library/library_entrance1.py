'''
Created on 2017年11月21日

@author: jack
'''
from Tools import MyLogger
from FeatureCalculaters import FeatureCalculater

class library_entrance1(FeatureCalculater.FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                计算每一学年图书馆进出
        '''
        student_num = str(self.student.getStudentId())
        for school_year in self.school_year:
            sql = "SELECT sum(seat_time) FROM library_study_time where student_num = " + student_num + " AND DAYOFYEAR(select_seat_time)=" + str(school_year)
            self.executer.execute(sql)
            library_study_time = self.executer.fetchone()[0]
            sql = "update students set library_study_time ='" + str(library_study_time) + "' where student_num=" + student_num + " AND school_year =" + str(school_year)
            self.executer.execute(sql)
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='library_entrance', clusters=4, sql="SELECT library_entrance FROM students WHERE library_entrance != 0")
        sql = "SELECT max(library_entrance) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "library_entrance" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
