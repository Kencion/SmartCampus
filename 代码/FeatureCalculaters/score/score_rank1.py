'''
Created on 2017年11月22日

@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater

class score_rank1(FeatureCalculater.FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                计算成绩排名
        '''
        sql = "select student_num from students"
        self.executer.execute(sql)
        sql = "select student_num from students"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            rank1 = 0
            rank2 = 0
            rank = 0
            stu_num = str(i[0])[:-4]
            school_year = str(i[0])[-4:]
            next_year = str(int(school_year) + 1)
            year1 = school_year + "/" + next_year + "-1"
            year2 = school_year + "/" + next_year + "-2"
            sql = "select Rank from score where stu_num = '" + stu_num + "' and school_year = '" + year1 + "'"  
            # print(sql)
            self.executer.execute(sql)
            stu1 = self.executer.fetchone()
            # print(stu1)
            if(stu1 is not None):
                rank1 = int(stu1[0])
            sql = "select Rank from score where stu_num = '" + stu_num + "' and school_year = '" + year2 + "'"
            self.executer.execute(sql)
            stu2 = self.executer.fetchone()
            if(stu2 is not None):
                rank2 = float(stu2[0])
            rank = (rank1 + rank2) / 2
            print(rank)
            sql = "update students set score_rank = " + str(rank) + " where student_num = '" + stu_num + school_year + "'"
            self.executer.execute(sql)
            
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='score_rank', clusters=4, sql="SELECT score_rank FROM students WHERE score_rank != 0")
        sql = "SELECT max(score_rank) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "score_rank" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()
