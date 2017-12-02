'''
Created on 2017年11月21日

@author: jack
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater


class subsidy_rank(FeatureCalculater):
        
    @MyLogger.myException
    def calculate(self):
        '''
                        计算获得奖学金的等级
        '''
        for school_year in self.school_year:
            student_num = str(self.student_num)
            sql = "SELECT rank FROM subsidy_handled where student_num = '{0}' AND grant_year='{1}'".format(student_num , school_year)
            self.executer.execute(sql)
            subsidy_rank = self.executer.fetchone()[0]
            sql = "update students set subsidy_rank ='" + str(subsidy_rank) + "' where student_num='" + student_num + str(school_year) + "'"
            self.executer.execute(sql)
        
    @MyLogger.myException
    def cluster(self):
        maxx, minn, cent = FeatureCalculater.cluster(self, featureName='subsidy_rank', clusters=4, sql="SELECT subsidy_rank FROM students WHERE subsidy_rank != 0")
        sql = "SELECT max(subsidy_rank) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("subsidy_rank" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
