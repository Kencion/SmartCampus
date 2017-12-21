'''
@author: yhj
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class participation_avg_point1(FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                计算活动参与平均分
        '''
#         sql="select stu_num,DATE_FORMAT(Start_time, '%Y'),sum(Participation_point)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y')"
#         self.executer.execute(sql)
#         result=self.executer.fetchall()
#         for re in result:
#             sql="update students set participation_avg_point=%s where student_num=%s"
#             self.executer.execute(sql,(double(re[2]),re[0]+str(int(re[1])-1)))
        sql = "select Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(Participation_point)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            re[1].split('-')
            if int(re[1][6:7]) < 9:
                sql = "update students set participation_avg_point=(participation_avg_point+%s)/2 where student_num=%s"
                self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
            else:
                sql = "update students set participation_avg_point=(participation_avg_point+%s)/2 where student_num=%s "
                self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
            
    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(participation_avg_point) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='participation_avg_point', clusters=4, sql="SELECT participation_avg_point FROM students WHERE participation_avg_point != 0")
        maxx[len(maxx) - 1] = max_num
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("participation_avg_point字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()     
