'''
Created on 2017年11月23日
 
@author: jack
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

 
class hornorary_times(FeatureCalculater):
         
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年内获得荣誉次数
        '''
#         student_num = str(self.student_num)
#         for school_year in self.school_year:
#             sql = "select count(*) from hornorary_handled where student_num='{0}' and left(grant_year,4)='{1}'".format(student_num, school_year)
#             self.executer.execute(sql)
#             hornorary_times = self.executer.fetchone()[0]
#             sql = "update students set hornorary_times ={0} where student_num='{1}'".format(hornorary_times, student_num + school_year)
#             self.executer.execute(sql)
#         student_num = str(self.student_num)
#         for school_year in self.school_year:
#             self.executer.execute("select count(*) from hornorary_handled where student_num=%s and grant_year=%s", (student_num, school_year + "-" + str(int(school_year) + 1)))
#             hornorary_times = self.executer.fetchone()[0]
#             self.executer.execute("update students set hornorary_times =%s where student_num=%s" , (hornorary_times, student_num + school_year))
        sql = "update students set hornorary_times=0"
        self.executer.execute(sql)
        sql = "select student_num,left(grant_year,4),count(*) from hornorary_handled group by student_num,left(grant_year,4)"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            sql = "update students set hornorary_times=%s where student_num=%s"
            self.executer.execute(sql, (re[2], (re[0] + re[1])))  
            
    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(hornorary_times) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='hornorary_times', clusters=2, sql="SELECT hornorary_times FROM students WHERE hornorary_times != 0")
        maxx[len(maxx) - 1] = max_num
         
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("hornorary_times字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()    
