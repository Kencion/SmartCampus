'''
@author: yhj
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
from boto.sdb.db.sequence import double

class activity_avg_level1(FeatureCalculater.FeatureCalculater):
    '''
            计算活动持续时间
    '''
    def setLevel(self):
        pass
        
    @MyLogger.myException
    def calculate(self):
        sql="select stu_num,DATE_FORMAT(Start_time, '%Y'),sum(Active_level)/count(*) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y')"
        self.executer.execute(sql)
        result=self.executer.fetchall()
        for re in result:
            sql="update students set activity_avg_level=%s where student_num=%s"
            self.executer.execute(sql,(double(re[2]),re[0]+str(int(re[1])-1)))
            #print(re[0]+str(int(re[1])-1))
        
        
    def cluster(self):
        sql="SELECT max(activity_avg_level) FROM students"
        self.executer.execute(sql)
        result=self.executer.fetchone()[0]
        max_num=int(result)
        maxx,minn,cent=FeatureCalculater.FeatureCalculater.cluster(self,featureName='activity_avg_level', clusters=4, sql="SELECT activity_avg_level FROM students WHERE activity_avg_level != 0")
        maxx[len(maxx) - 1] = max_num
        
        with open(r"聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write( "activity_avg_level字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            print("write.....")
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()    
