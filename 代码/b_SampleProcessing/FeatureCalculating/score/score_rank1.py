'''
Created on 2017年11月22日

@author: yzh
'''
from z_Tools import MyLogger
from b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater

class score_rank1(FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                    计算成绩排名
        '''
        sql = "select distinct(stu_num),grade from score"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
#             print(str(i[0]))
            stu_num = str(i[0])
            grade = int(i[1])
            for year in range(grade,2017):
                rank1 = 0
                rank2 = 0
                rank = 0
                year1 = str(year)+'/'+str(year+1)+'-1'
                year2 = str(year)+'/'+str(year+1)+'-2'
                sql = "select rank from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"   
#                 print(sql)
                self.executer.execute(sql)
                stu1 = self.executer.fetchone()
#                 print(stu1)
                
                if stu1 is not None :
                    rank1 = int(stu1[0])
                    
                sql = "select rank from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"   
#                 print(sql)
                self.executer.execute(sql)
                stu2 = self.executer.fetchone()
#                 print(stu2)
                if stu2 is not None:
                    rank2 = int(stu2[0])
                    
                if stu1 is not None and stu2 is not None: 
                    rank = int((rank1 + rank2)/2)
                    sql = "update students set score_rank = "+str(rank)+" where student_num = '"+stu_num+str(year)+"'"
#                     print(sql)
                    self.executer.execute(sql)
#         print("ok")
        
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.cluster(self,featureName='score_rank', clusters=4, sql="SELECT score_rank FROM students WHERE score_rank != NULL")
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
            
# score_rank = score_rank1()
# score_rank.calculate()