'''
 
@author: yzh
'''
from Tools import *
from FeatureCalculaters import FeatureCalculater
from numpy import float16, double, append
from sklearn.cluster import KMeans
import numpy
 
class score1(FeatureCalculater.FeatureCalculater):
    
    def calculate(self):
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
        
    @MyLogger.myException
    def cluster(self, clusters=4):
        # 上面那个地方其实是没错的，但是eclipse会报错。那个是python3.x的参数注解，不信百度去。
        
        # 获得学生的数据
        dataSet = []
        sql = "SELECT score FROM students WHERE score != 0"
        count = self.executer.execute(sql)  # count是行数
        result = self.executer.fetchall()
        for i in result:
            dataSet.append(i[0])  # 根据数据库表中的字段取精度
        dataSet = numpy.array(dataSet).reshape(count, 1)
        # 聚类
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(dataSet)  
        # 求出聚类中心
        center = kmeans.cluster_centers_
        center_x = ['%0.4f' % center[i][0] for i in range(len(center))]
        # 标注每个点的聚类结果
        labels = kmeans.labels_ 
        types, maxx, minn = [[] for i in range(0, clusters)], [], []
            
        for i in range(len(labels)):
            types[labels[i]].append(dataSet[i][0])
            sql = "update students_rank set score='" + str(labels[i] + 1) + "' where score=" + str(dataSet[i][0]) 
            self.executer.execute(sql)
            
        print(types)
        
        for i in range(0, clusters):
            maxx.append(max(types[i]))
            minn.append(min(types[i]))
        
        with open(r"聚类对应的字段区间", "a", encoding='utf8') as f:
            f.write('score字段' + '\n')
            for i in range(len(center)):
                f.write(str(i) + ':' + ' ' + str(center[i][0]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
            f.close()

t = score1()
t.cluster(4)
