'''
Created on 2017年11月23日

@author: yzh
'''

from Tools import *
from FeatureCalculaters import FeatureCalculater

class is_social_practice_great1(FeatureCalculater.FeatureCalculater):
    
    @MyLogger.myException
    def calculate(self):
        '''
                判断是否是院级或者校级重点。
                思路：从social_practice表中获取student_num以及学年（根据start_time来划分），是否是重点，然后根据stu_num关键字填入students表中。
        '''
        sql = "select stu_num,DATE_FORMAT(start_time,'%Y'),DATE_FORMAT(start_time,'%c'),School_key_projects_or_not,College_key_projects_or_not from social_practice"
        self.executer.execute(sql)
        e = self.executer.fetchall()
        for i in e:
            stu_num = str(i[0])
            year = int(i[1])
            month = int(i[2])
            if(month<9):
                year = year - 1
            School_key_projects_or_not = i[3]
            College_key_projects_or_not = i[4]
            if(School_key_projects_or_not == "否" and College_key_projects_or_not =="否"):
                is_social_practice_great = 0
            else:
                is_social_practice_great = 1
            sql = "update students set is_social_practice_great = '"+str(is_social_practice_great)+"' where student_num = '"+str(stu_num)+str(year)+"'"
            self.executer.execute(sql)
            
    @MyLogger.myException
    def cluster(self):
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='is_social_practice_great', clusters=4, sql="SELECT is_social_practice_great FROM students WHERE is_social_practice_great != 0")
        sql = "SELECT max(is_social_practice_great) FROM students"
        self.executer.execute(sql)
        maxx[len(maxx) - 1] = self.executer.fetchone()[0]
        
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write( "is_social_practice_great" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()