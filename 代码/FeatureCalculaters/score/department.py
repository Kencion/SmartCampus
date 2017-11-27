'''
Created on 2017年11月23日

@author: jack
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class department(FeatureCalculater.FeatureCalculater):

    @MyLogger.myException
    def calculate(self):
        '''
                        计算学生的系别
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select department from score where student_num=%s", (student_num))
            department = self.executer.fetchone()[0]
            self.executer.execute("update students set hornorary_rank =%s where student_num=%s" , (department, student_num + school_year))
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='department', clusters=4, sql="SELECT department FROM students WHERE department != 0")
        sql = "SELECT max(department) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "department" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
