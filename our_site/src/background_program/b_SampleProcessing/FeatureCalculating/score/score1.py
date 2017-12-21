'''
 
@author: yzh
'''
from background_program.z_Tools import MyLogger
from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
 
class score1(FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                            计算成绩
                            从score表中取出信息，按照score表中的学号索取到students表的学号，再将成绩信息填充到students表中。
            score = (score1*学分1+score2*学分2)/(学分1+学分2)
        '''
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
                    self.executer.execute(sql)
        print("ok")
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.cluster(self,featureName='score', clusters=4, sql="SELECT score FROM students WHERE score is not NULL")
        maxx[len(maxx) - 1] = 100
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "score字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
# score = score1()
# score.calculate()