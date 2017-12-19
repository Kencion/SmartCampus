'''
Created on 2017年11月21日

@author: jack
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class scholarship_rank(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                计算获得奖学金的等级
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT scholarship_type FROM scholarship_handled where student_num ='{0}' AND left(grant_year,4)='{1}'".format(str(student_num) , str(school_year))
            self.executer.execute(sql)
            try: 
                scholarship_ranks = self.executer.fetchall()
                scholarship_rank = 0
                for i in scholarship_ranks:
                    if i[0] == '国家奖学金':
                        scholarship_rank += 19
                    elif i[0] == '本科生优秀学生奖学金':
                        scholarship_rank += 17
                    elif i[0] == '校级奖学金':
                        scholarship_rank += 15
                    elif i[0] == '国家励志奖学金':
                        scholarship_rank += 13
                    elif i[0] == '奖学金':
                        scholarship_rank += 11
                    elif i[0] == '其他来源奖学金':
                        scholarship_rank += 9
                    elif i[0] == '-三大奖校级奖学金':
                        scholarship_rank += 7
            except:
                scholarship_rank = 0
            sql = "update students set scholarship_rank ='{0}' where student_num='{1}'".format(scholarship_rank, student_num + str(school_year))
            self.executer.execute(sql)
        
    @MyLogger.myException
    def cluster(self):
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='scholarship_rank', clusters=4, sql="SELECT scholarship_rank FROM students WHERE scholarship_rank != 0")
        sql = "SELECT max(scholarship_rank) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("scholarship_rank" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
