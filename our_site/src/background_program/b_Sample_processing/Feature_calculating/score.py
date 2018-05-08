from background_program.z_Tools.my_exceptions import my_exception_handler
from .FeatureCalculater import FeatureCalculater


class department(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='hornorary_rank')

    @my_exception_handler
    def calculate(self):
        '''
                        计算学生的系别
        '''
        sql = "SELECT DISTINCT student_num FROM score"
        self.executer.execute(sql)
        student_nums = [str(i[0]) for i in self.executer.fetchall()]
        for student_num in student_nums:
            self.school_year = self.get_school_year(student_num)
            for school_year in self.school_year:
                sql = "select department from score where student_num='{0}'".format(student_num)
                self.executer.execute(sql)
                try:
                    department = self.executer.fetchone()[0]
                except:
                    pass
                sql = "update students set hornorary_rank ={0} where student_num='{1}'".format(department, student_num + school_year)
                if self.executer.execute(sql) == 0:
                    self.add_student(student_num + str(school_year))
                    self.executer.execute(sql)
        
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class failed_failed_num(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='activity_avg_level')

    @my_exception_handler
    def calculate(self):
        '''
                            计算failed_failed_num：挂科重修后任然没通过的数目
                            从students表中取出信息，按照students表的学号，再将挂科信息填充到students表中。
        '''
        sql = "select student_num,failed_num,failed_pass_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            failed_failed_num = 0
            if i[1] is not None and i[2] is not None:
                student_num = str(i[0])
                failed_num = int(i[1])
                failed_pass_num = int(i[2])
                failed_failed_num = failed_num - failed_pass_num
                sql = "update students set failed_failed_num = '" + str(failed_failed_num) + "' where student_num = '" + str(student_num) + "'"
                self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class failed_num1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='failed_num')
    
    @my_exception_handler
    def calculate(self):
        '''
                            计算挂科的数目
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将挂科信息填充到students表中。
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                failed_num1 = 0
                pass_num1 = 0
                failed_num2 = 0
                pass_num2 = 0
                failed_num = 0
                pass_num = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None :
                    failed_num1 = int(stu1[0])
                    pass_num1 = int(str(stu1[1])[:-1])
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"   
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None:
                    failed_num2 = int(stu2[0])
                    pass_num2 = int(str(stu2[1])[:-1])
                    
                failed_num = failed_num1 + failed_num2
                pass_num = pass_num1 + pass_num2
                sql = "update students set failed_num = " + str(failed_num) + " where student_num = '" + stu_num + str(year) + "'"

                t = self.executer.execute(sql)
                if t == 0:
                    self.add_student(stu_num + str(year))
                    self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class failed_pass_num(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='failed_pass_num')
    
    @my_exception_handler
    def calculate(self):
        '''
                            计算挂科重修过的数目
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将成绩信息填充到students表中。
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                failed_num1 = 0
                pass_num1 = 0
                failed_num2 = 0
                pass_num2 = 0
                failed_num = 0
                pass_num = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None :
                    failed_num1 = int(stu1[0])
                    pass_num1 = int(str(stu1[1])[:-1])
                sql = "select substring_index(failed_num,'(',1),substring_index(failed_num,'(',-1) from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"   
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None:
                    failed_num2 = int(stu2[0])
                    pass_num2 = int(str(stu2[1])[:-1])
                    
                failed_num = failed_num1 + failed_num2
                pass_num = pass_num1 + pass_num2
                sql = "update students set failed_pass_num = " + str(pass_num) + " where student_num = '" + stu_num + str(year) + "'"
                t = self.executer.execute(sql)
                if t == 0:
                    self.add_student(stu_num + str(year1))
                    self.executer.execute(sql)

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class GPA1(FeatureCalculater):
    
    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='GPA')

    @my_exception_handler
    def calculate(self):
        '''
                            计算GPA
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将GPA信息填充到students表中。
        GPA = (GPA1*学分1+GPA2*学分2)/(学分1+学分2)
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                GPA1 = 0
                credit1 = 0
                GPA2 = 0
                credit2 = 0
                GPA = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select GPA,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None and stu1[0] is not None:
                    GPA1 = float(stu1[0])
                    credit1 = int(stu1[1])
                sql = "select GPA,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"  
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None and stu2[0] is not None:
                    GPA2 = float(stu2[0])
                    credit2 = int(stu2[1])
                if((credit1 + credit2) != 0):
                    GPA = (GPA1 * credit1 + GPA2 * credit2) / (credit1 + credit2)
                    sql = "update students set GPA = " + str(GPA) + " where student_num = '" + stu_num + str(year) + "'"
                    t = self.executer.execute(sql)
                    if t == 0:
                        self.add_student(stu_num + str(year))
                        self.executer.execute(sql)

    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class school_year1(FeatureCalculater):
    
    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='school_year')

    @my_exception_handler
    def calculate(self):
        '''
                计算获得奖学金的金额
        '''
        sql = "select DISTINCT stu_num,left(school_year, 9) from score"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        print(result)
        for re in result:
            str(re[1]).split('/')
            sql = "update students set school_year=%s where student_num=%s"
            self.executer.execute(sql, (re[1], str(re[0]) + re[1][0:4]))
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)


class score_rank1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='score_rank')
    
    @my_exception_handler
    def calculate(self):
        '''
                    计算成绩排名
                    从score表中取出信息，按照score表中的学号索取到students表的学号，再将成绩排名信息填充到students表中。
        rank = (rank1+rank2)/2 取算术平均
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade, 2017):
                rank1 = 0
                rank2 = 0
                rank = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select rank from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None :
                    rank1 = int(stu1[0])
                    
                sql = "select rank from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"   
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None:
                    rank2 = int(stu2[0])
                    
                if stu1 is not None and stu2 is not None: 
                    rank = int((rank1 + rank2) / 2)
                    sql = "update students set score_rank = " + str(rank) + " where student_num = '" + stu_num + str(year) + "'"
                    
                    t = self.executer.execute(sql)
                    if t == 0:
                        self.add_student(stu_num + str(year))
                        self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
        

class score1(FeatureCalculater):

    def __init__(self):
        FeatureCalculater.__init__(self, feature_name='score')
    
    @my_exception_handler
    def calculate(self):
        '''
                            计算成绩
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将成绩信息填充到students表中。
            score = (score1*学分1+score2*学分2)/(学分1+学分2)
        '''
#         print("start")
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            
            grade = int(i[1])
            for year in range(grade, 2017):
                score1 = 0
                credit1 = 0
                score2 = 0
                credit2 = 0
                score = 0
                year1 = str(year) + '/' + str(year + 1) + '-1'
                year2 = str(year) + '/' + str(year + 1) + '-2'
                sql = "select score,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"   
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
                
                if stu1 is not None and stu1[0] is not None:
                    score1 = float(stu1[0])
                    credit1 = int(stu1[1])
                    
                sql = "select score,course_credit from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"  
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
                if stu2 is not None and stu2[0] is not None:
                    score2 = float(stu2[0])
                    credit2 = int(stu2[1])
                if((credit1 + credit2) != 0):
                    score = (score1 * credit1 + score2 * credit2) / (credit1 + credit2)
                    sql = "update students set score = " + str(score) + " where student_num = '" + stu_num + str(year) + "'"
                    
                    t = self.executer.execute(sql)
                    if t == 0:
                        self.add_student(stu_num + str(year))
                        self.executer.execute(sql)
    
    def cluster(self):
        FeatureCalculater.cluster(self, clusters=4)
