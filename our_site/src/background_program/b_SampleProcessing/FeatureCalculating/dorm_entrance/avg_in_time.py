'''
@author: yhj
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class avg_in_time(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        sql = "select student_num,avg(max_day_in_time) from dorm_entrance_handled where week_num='6' or week_num='7' group by student_num,DATE_FORMAT(date, '%Y') "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set avg_in_time=%s where student_num=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))
    
    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(avg_in_time) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='avg_in_time', clusters=4, sql="SELECT avg_in_time FROM students WHERE avg_in_time != 0")
        maxx[len(maxx) - 1] = max_num
         
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("avg_in_time字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close() 
