'''
@author: yhj
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
from boto.sdb.db.sequence import double

class activity_last_time1(FeatureCalculater):
    '''
            计算活动持续时间
    '''
        
    @MyLogger.myException
    def calculate(self):
        sql = "update students set activity_last_time=%s"
        self.executer.execute(sql, double(0))
        sql = "select Distinct Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(time_to_sec(timediff(Finish_time,Start_time))) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
#         print(result)
        for re in result:
            re[1].split('-')
            if int(re[1][6:7]) < 9:
                sql = "update students set activity_last_time=activity_last_time+%s where student_num=%s"
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
            else:
                sql = "update students set activity_last_time=activity_last_time+%s where student_num=%s "
                self.executer.execute(sql, (double(re[2]), str(re[0]) + (str)(re[1][0:4])))
    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(activity_last_time) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='activity_last_time', clusters=4, sql="SELECT activity_last_time FROM students WHERE activity_last_time != 0")
        maxx[len(maxx) - 1] = max_num
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("activity_last_time字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()     
