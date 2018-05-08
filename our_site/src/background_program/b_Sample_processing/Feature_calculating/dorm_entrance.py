from background_program.z_Tools.my_exceptions import my_exception_handler
from .FeatureCalculater import FeatureCalculater


class avg_in_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='avg_in_time')
        
    @my_exception_handler
    def calculate(self):
        sql = "select student_num,avg(max_day_in_time) from dorm_entrance_handled where week_num='6' or week_num='7' group by student_num "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            if re is None:
                pass
            else:
                sql = "update students set avg_in_time=%s where student_num=%s"
                num = self.executer.execute(sql, (float(re[1]), re[0]))
                if num == 0:
                    self.add_student(re[0])
                    self.executer.execute(sql, (float(re[1]), re[0]))

    def add(self):
        sql = "SELECT left(student_num,14),avg(avg_in_time) from students where avg_in_time!=0 group by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set avg_in_time=%s where left(student_num,14)=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class avg_out_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='avg_out_time')

    @my_exception_handler
    def calculate(self):
        
        # 分组计算每天出门的最早时间
        sql = "select student_num,DATE_FORMAT(record_time, '%Y-%m'),DATE_FORMAT(record_time, '%Y-%m-%d'),TIME_TO_SEC(DATE_FORMAT((min(record_time)),'%H:%m:%s')),DAYOFWEEK(DATE_FORMAT(record_time, '%Y-%m-%d'))-1 from dorm_entrance where in_out='出门'  group by student_num,DATE_FORMAT(record_time, '%Y-%m-%d') having min(DATE_FORMAT(record_time, '%H'))>5 order by student_num"
        self.executer.execute(sql)
        re = self.executer.fetchall()
        for r in re:
            if int(r[4]) == 0:
                r[1].split('-')
                if int(r[1][5:7]) < 9:
                    sql = "insert into dorm_entrance_handled(student_num,date,min_day_out_time,week_num) values(%s,%s,%s,%s)"
                    self.executer.execute(sql, (r[0] + (str)(int(r[1][0:4]) - 1), r[2], r[3], int(7)))
                else:
                    sql = "insert into dorm_entrance_handled(student_num,date,min_day_out_time,week_num) values(%s,%s,%s,%s)"
                    self.executer.execute(sql, (r[0] + (str)(int(r[1][0:4])), r[2], r[3], int(7)))
            else:
                r[1].split('-')
                if int(r[1][5:7]) < 9:
                    sql = "insert into dorm_entrance_handled(student_num,date,min_day_out_time,week_num) values(%s,%s,%s,%s)"
                    self.executer.execute(sql, (r[0] + (str)(int(r[1][0:4]) - 1), r[2], r[3], int(r[4])))
                else:
                    sql = "insert into dorm_entrance_handled(student_num,date,min_day_out_time,week_num) values(%s,%s,%s,%s)"
                    self.executer.execute(sql, (r[0] + (str)(int(r[1][0:4])), r[2], r[3], int(r[4])))
        # 分组计算每天进门的最晚时间
        sql = "select student_num,DATE_FORMAT(record_time, '%Y-%m'),DATE_FORMAT(record_time, '%Y-%m-%d'),TIME_TO_SEC(DATE_FORMAT((max(record_time)),'%H:%m:%s')) from dorm_entrance where in_out='进门'  group by student_num,DATE_FORMAT(record_time, '%Y-%m-%d')  order by student_num"
        self.executer.execute(sql)
        re = self.executer.fetchall()
        for r in re:
            r[1].split('-')
            if int(r[1][5:7]) < 9:
                sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and date=%s"
                self.executer.execute(sql, (float(r[3]), r[0] + (str)(int(r[1][0:4]) - 1), r[2]))
            else:
                sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and date=%s"
                self.executer.execute(sql, (float(r[3]), r[0] + (str)(int(r[1][0:4])), r[2]))
         
        # 根据出门情况，用平均值补进门时间的缺失值
        sql = "select student_num,avg(max_day_in_time) from dorm_entrance_handled group by student_num"
        self.executer.execute(sql)
        res = self.executer.fetchall()
        for r in res:
            sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and max_day_in_time=%s"
            self.executer.execute(sql, (float(r[1]), r[0], float(0)))
     
#         #计算是否凌晨回宿舍
        sql = "select student_num,DATE_FORMAT(record_time, '%Y-%m'),date_sub(DATE_FORMAT((record_time),'%Y-%m-%d'), interval 1 day),TIME_TO_SEC(DATE_FORMAT((record_time),'%H:%m:%s')) from dorm_entrance where in_out='进门' group by student_num,DATE_FORMAT(record_time, '%Y-%m-%d') having min(DATE_FORMAT(record_time, '%H'))<" + str(4)
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            re[1].split('-')
            if int(re[1][5:7]) < 9: 
                sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and date=%s"
                self.executer.execute(sql, ((float(re[3]) + 86400), re[0] + (str)(int(re[1][0:4]) - 1), re[2]))
            else:
                sql = "update dorm_entrance_handled set max_day_in_time=%s where student_num=%s and date=%s"
                self.executer.execute(sql, ((float(re[3]) + 86400), re[0] + (str)(int(re[1][0:4])), re[2]))
# #         #求年平均周末最早出门时间
        sql = "select student_num,avg(min_day_out_time) from dorm_entrance_handled where week_num='6' or week_num='7' group by student_num "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            if re is None:
                pass
            else:
                sql = "update students set avg_out_time=%s where student_num=%s"
                num = self.executer.execute(sql, (float(re[1]), re[0]))
                if num == 0:
                    self.add_student(re[0])
                    self.executer.execute(sql, (float(re[1]), re[0]))
    
    def add(self):
        sql = "SELECT left(student_num,14),avg(avg_out_time) from students where avg_out_time!=0 group by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set avg_out_time=%s where left(student_num,14)=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class avg_stay_out_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='avg_stay_out_time')

    @my_exception_handler
    def calculate(self):
        sql = "select student_num,avg(max_day_in_time-min_day_out_time) from dorm_entrance_handled where week_num!='6' and week_num!='7' group by student_num "
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            if re is None:
                pass
            else:
                sql = "update students set avg_stay_out_time=%s where student_num=%s"
                num = self.executer.execute(sql, (float(re[1]), re[0]))
                if num == 0:
                    self.add_student(re[0])
                    self.executer.execute(sql, (float(re[1]), re[0]))

    def add(self):
        sql = "SELECT left(student_num,14),avg(avg_stay_out_time) from students where avg_stay_out_time!=0 group by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set avg_stay_out_time=%s where left(student_num,14)=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)

        
class in_out_times(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='in_out_times')

    @my_exception_handler
    def calculate(self):
        '''
                计算一学年进出宿舍次数
        '''
        sql = "update students set in_out_times=%s"
        self.executer.execute(sql, float(0))
        sql = "SELECT DISTINCT student_num FROM dorm_entrance"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year = self.get_school_year(student_num)
            for school_year in self.school_year:
                self.executer.execute("select count(*),DATE_FORMAT(record_time,'%m') from dorm_entrance where student_num='{0}' and DATE_FORMAT(record_time,'%Y')='{1}'".format(student_num, school_year))
                try:
                    result = self.executer.fetchone()
                    in_out_times, month = result[0], result[1]
                    if int(month) < 9:
                        school_year = int(school_year) - 1
                except:
                    continue
                sql = "update students set in_out_times ={0} where student_num='{1}'" .format (int(in_out_times), student_num + str(school_year))
                if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)

    def add(self):
        sql = "SELECT left(student_num,14),avg(in_out_times) from students where in_out_times!=0 group by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall() 
        for re in result:
            sql = "update students set in_out_times=%s where left(student_num,14)=%s"
            self.executer.execute(sql, (float(re[1]), re[0]))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
