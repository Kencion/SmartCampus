'''
@author: yhj
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class avg_out_time(FeatureCalculater):

    def calculate(self):
        
        # 分组计算每天出门的最早时间
        sql = "select student_num,DATE_FORMAT(record_time, '%Y'),DATE_FORMAT(record_time, '%Y-%m-%d'),TIME_TO_SEC(DATE_FORMAT((min(record_time)),'%H:%m:%s')),DAYOFWEEK(DATE_FORMAT(record_time, '%Y-%m-%d'))-1 from dorm_entrance where in_out='出门'  group by student_num,DATE_FORMAT(record_time, '%Y-%m-%d') having min(DATE_FORMAT(record_time, '%H'))>5 order by student_num"
        self.executer.execute(sql)
        re = self.executer.fetchall()
        for r in re:
            if int(r[4]) == 0:
                sql = "insert into dorm_entrance_handled(student_num,date,min_day_out_time,week_num) values(%s,%s,%s,%s)"
                self.executer.execute(sql, (r[0] + str(int(r[1]) - 1), r[2], r[3], int(7)))
            else:
                sql = "insert into dorm_entrance_handled(student_num,date,min_day_out_time,week_num) values(%s,%s,%s,%s)"
                self.executer.execute(sql, (r[0] + str(int(r[1]) - 1), r[2], r[3], int(r[4])))
        # 分组计算每天进门的最晚时间
        sql = "select student_num,DATE_FORMAT(record_time, '%Y'),DATE_FORMAT(record_time, '%Y-%m-%d'),TIME_TO_SEC(DATE_FORMAT((max(record_time)),'%H:%m:%s')) from dorm_entrance where in_out='进门'  group by student_num,DATE_FORMAT(record_time, '%Y-%m-%d')  order by student_num"
        self.executer.execute(sql)
        re = self.executer.fetchall()
        for r in re:
            sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and date=%s"
            self.executer.execute(sql, (float(r[3]), r[0] + str(int(r[1]) - 1), r[2]))
         
        # 根据出门情况，用平均值补进门时间的缺失值
        sql = "select student_num,avg(max_day_in_time) from dorm_entrance_handled group by student_num,DATE_FORMAT(date, '%Y')"
        self.executer.execute(sql)
        res = self.executer.fetchall()
        for r in res:
            sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and max_day_in_time=%s"
            self.executer.execute(sql, (float(r[1]), r[0], float(0)))
     
#         #计算是否凌晨回宿舍
        sql = "select student_num,DATE_FORMAT(record_time, '%Y'),date_sub(DATE_FORMAT((record_time),'%Y-%m-%d'), interval 1 day),TIME_TO_SEC(DATE_FORMAT((record_time),'%H:%m:%s')) from dorm_entrance where in_out='进门' group by student_num,DATE_FORMAT(record_time, '%Y-%m-%d') having min(DATE_FORMAT(record_time, '%H'))<" + str(4)
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and date=%s"
            self.executer.execute(sql, ((float(re[3]) + 86400), re[0] + str(int(re[1]) - 1), re[2]))
# #         #求年平均周末最早出门时间
        sql = "select student_num,avg(min_day_out_time) from dorm_entrance_handled where week_num='6' or week_num='7' group by student_num,DATE_FORMAT(date, '%Y') "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set avg_out_time=%s where student_num=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))

    @MyLogger.myException
    def cluster(self):
        sql = "SELECT max(avg_out_time) FROM students"
        self.executer.execute(sql)
        result = self.executer.fetchone()[0]
        max_num = int(result)
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='avg_out_time', clusters=4, sql="SELECT avg_out_time FROM students WHERE avg_out_time != 0")
        maxx[len(maxx) - 1] = max_num
         
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("avg_out_time字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close() 
