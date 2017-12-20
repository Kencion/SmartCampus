'''
Created on 2017年11月23日

@author: jack
'''
'''
@author: yhj
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class in_out_times(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算一学年进出宿舍次数
        '''
        student_num = str(self.student_num)
        for school_year in self.school_year:
            self.executer.execute("select count(*),DATE_FORMAT(record_time,'%m') from dorm_entrance where student_num='{0}' and DATE_FORMAT(record_time,'%Y')='{1}'".format(student_num, school_year))
            try:
                result = self.executer.fetchone()[0]
                in_out_times, month = result[0], result[1]
                if int(month) < 9:
                    school_year = int(school_year) - 1
            except:
                in_out_times = 0
            sql = "update students set in_out_times ='{0}' where student_num='{1}'" .format (int(in_out_times), student_num + str(school_year))
            self.executer.execute(sql)

    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(in_out_times) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='in_out_times', clusters=4, sql="SELECT in_out_times FROM students WHERE in_out_times != 0")
        maxx[len(maxx) - 1] = max_num
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("in_out_times字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()     
