from background_program.z_Tools.my_exceptions import my_exception_handler
from .FeatureCalculater import FeatureCalculater


class ScholarAmount(FeatureCalculater):
    """
        将student_float表中的scholarship_amount二分类进student_int表
    0表示未获得奖学金，1表示获得奖学金
    """

    def Classifier(self):
        sql = "SELECT student_num,sum(scholarship_amount) FROM students_float  group by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        for re in result:
            if int(re[1]) != 0:
                re[1] = 1
            else:
                re[1] = 0
            sql = "update students_int set scholarship_amount = {0} where student_num = {1}".format(float(re[1]), str(re[0])) 
            n_update = self.executer.execute(sql)
            if n_update == 0:
                try:
                    sql = 'insert into students_int(student_num) values({0})'.format(str(re[0]))
                    self.executer.execute(sql)
                except:
                    pass
                sql = "update students_int set scholarship_amount= {0} where student_num = {1}".format(float(re[1]), str(re[0])) 
                self.executer.execute(sql)


class SubAmount(FeatureCalculater):
    """
        将student_float表中的subdisy_amount二分类进student_int表
    0表示未获得助学金，1表示获得助学金
    """

    def Classifier(self):
        sql = "SELECT student_num,sum(subsidy_amount) FROM students_float  group by student_num"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        num = 0
        for re in result:
            if int(re[1]) != 0:
                num = 1
            else:
                num = 0
            sql = "update students_int set subsidy_amount = {0} where student_num = {1}".format(float(num), str(re[0])) 
            n_update = self.executer.execute(sql)
            if n_update == 0:
                try:
                    sql = 'insert into students_int(student_num) values({0})'.format(str(re[0]))
                    self.executer.execute(sql)
                except:
                    pass
                sql = "update students_int set  subsidy_amount= {0} where student_num = {1}".format(float(num), str(re[0])) 
                self.executer.execute(sql)
