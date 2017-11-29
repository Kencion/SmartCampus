'''
Created on 2017年11月23日

@author: jack
'''
from Tools import MyLogger
from FeatureCalculaters import FeatureCalculater

class in_out_times(FeatureCalculater.FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年进出宿舍次数
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select count(*) from dorm_entrance where student_num='" + student_num + "' and DATE_FORMAT(record_time,'%Y')='" + school_year + "'")
            in_out_times = self.executer.fetchone()[0]
            if in_out_times != 0:
                print(in_out_times)
            self.executer.execute("update students set in_out_times =%s where student_num=%s" , (int(in_out_times), student_num + school_year))

    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(in_out_times) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.FeatureCalculater.cluster(self, featureName='in_out_times', clusters=4, sql="SELECT in_out_times FROM students WHERE in_out_times != 0")
        maxx[len(maxx) - 1] = max_num
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("in_out_times字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()     
