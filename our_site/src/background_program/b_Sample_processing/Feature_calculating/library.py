from background_program.z_Tools.my_exceptions import my_exception_handler
from .FeatureCalculater import FeatureCalculater


class library_borrow_times1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_borrow_times')
        
    @my_exception_handler
    def calculate(self):
        '''
                计算图书馆借阅
        '''
        sql = "select student_num,DATE_FORMAT(borrow_date, '%Y-%m'),count(*) from library_borrow group by student_num,DATE_FORMAT(borrow_date, '%Y-%m')"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        sql = "update students set library_borrow_times=0"
        self.executer.execute(sql)
        for re in result:
            if re is None:
                pass
            else:
                re[1].split('-')
                if int(re[1][5:7]) < 9:
                    sql = "update students set library_borrow_times=library_borrow_times+%s where student_num=%s"
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4]) - 1))
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(int(re[1][0:4]) - 1)))
                else:
                    sql = "update students set library_borrow_times=library_borrow_times+%s where student_num=%s"
                    num = self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))
                    if num == 0:
                        self.add_student(str(re[0]) + (str)(int(re[1][0:4])))
                        self.executer.execute(sql, (float(re[2]), str(re[0]) + (str)(re[1][0:4])))

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class library_entrance(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_study_time')
    
    @my_exception_handler
    def calculate(self):
        '''
                计算每一学年图书馆进出
        '''
        sql = "SELECT DISTINCT student_num FROM library_study_time"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year = self.get_school_year(student_num)
            for school_year in self.school_year:
                try:
                    sql = "SELECT sum(seat_time) FROM library_study_time where student_num = " + student_num + " AND DAYOFYEAR(select_seat_time)=" + str(school_year)
                    self.executer.execute(sql)
                    library_study_time = self.executer.fetchone()[0]
                    sql = "update students set library_study_time ='" + str(library_study_time) + "' where student_num=" + student_num + str(school_year)
                    if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)
                except:
                    pass
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class library_study_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_study_time')
        
    @my_exception_handler
    def calculate(self):
        '''
                        计算每一学年图书馆学习时间
        '''
        sql = "update students set library_study_time=%s"
        self.executer.execute(sql, float(0))
        sql = "SELECT DISTINCT student_num FROM library_study_time"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year = self.get_school_year(student_num)
            for school_year in self.school_year:
                sql = "SELECT sum(seat_time),DATE_FORMAT(select_seat_time,'%m') FROM library_study_time where student_num = '" + student_num + "' AND DATE_FORMAT(select_seat_time,'%Y')=" + str(school_year)
                self.executer.execute(sql)
                try:
                    result = self.executer.fetchone()
                    library_study_time, month = result[0], result[1]
                    if int(month) < 9:
                        school_year = int(school_year) - 1
                    sql = "update students set library_study_time =" + str(library_study_time) + " where student_num='" + student_num + str(school_year) + "'"
                    if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)
                except:
                    pass   
         
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class library_week_study_time(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='library_week_study_time')

    @my_exception_handler
    def calculate(self):
        '''
                        计算每一学年周末图书馆学习时间
        '''
        sql = "update students set library_week_study_time=%s"
        self.executer.execute(sql, float(0))
        sql = "SELECT DISTINCT student_num FROM library_study_time"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year = self.get_school_year(student_num)
            for school_year in self.school_year:
                sql = "SELECT sum(seat_time),DATE_FORMAT(select_seat_time,'%m') FROM library_study_time where student_num ='{0}' AND DATE_FORMAT(select_seat_time,'%Y')='{1}' AND DAYOFWEEK(select_seat_time) in (6,7)".format(student_num, str(school_year))
                self.executer.execute(sql)
                result = self.executer.fetchone()
                library_week_study_time, month = result[0], result[1]
                if library_week_study_time is not None:
                    sql = "update students set library_week_study_time =" + str(library_week_study_time) + " where student_num='" + student_num + str(school_year) + "'"
                    if self.executer.execute(sql) == 0:
                        self.add_student(student_num + str(school_year))
                        self.executer.execute(sql)
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
