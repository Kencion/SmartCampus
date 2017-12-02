'''
@author: jack
'''
from z_Tools import MyDataBase, MyLogger
from sklearn.cluster import KMeans
import numpy
 
class FeatureCalculater:
    '''
            特征计算器的父类
    '''
    def __init__(self, database="软件学院"):
        self.db = MyDataBase.MyDataBase(database)
        self.executer = self.db.getExcuter()
        self.school_year = ['2013', '2014', '2015', '2016', '2017', ]  # 一个同学一个学年作为一个记录
        self.level = None
                 
    def setStudentNum(self, student_num):
        '''
                        设置学生学号
        @params string student_num:学生学号
        @retrun
        '''
        self.student_num = student_num  # 学号
         
    @MyLogger.myException
    def calculate(self):
        '''
                        所有子类都要实现这个函数
                        特征值的计算
        @params 
        @retrun
        '''
        pass  
     
#     @MyLogger.myException
    def cluster(self, featureName , clusters=4, sql=""):
        '''
                        所有子类都要实现这个函数
                        对特征值进行聚类来归一化处理
        @params string featureName:特征名字,number clusters:要聚成几类,string sql:会用到的sql语句
        @retrun
        '''
        # 获得学生的数据
        self.dataSet = []
        count = self.executer.execute(sql)  # count是行数
        result = self.executer.fetchall()
        for i in result:
            self.dataSet.append(i[0])  # 根据数据库表中的字段取精度
        self.dataSet = numpy.array(self.dataSet).reshape(count, 1)
        # 聚类
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(self.dataSet)  
        # 求出聚类中心
        center = kmeans.cluster_centers_
        center_x = ['%0.4f' % center[i][0] for i in range(len(center))]
        # 标注每个点的聚类结果
        labels = kmeans.labels_ 
        types, maxx, minn = [[] for i in range(0, clusters)], [], []
            
        for i in range(len(labels)):
            types[labels[i]].append(self.dataSet[i][0])
            sql = "update students_rank set " + featureName + "='" + str(labels[i] + 1) + "' where " + featureName + "=" + str(self.dataSet[i][0]) 
            self.executer.execute(sql)
        
        for i in range(0, clusters):
            maxx.append(max(types[i]))
            minn.append(min(types[i]))
            
        maxx = sorted(maxx)
        minn = sorted(minn)
        center_x = [float(i) for i in center_x]
        cent = sorted(center_x)
        for i in range(len(maxx) - 1):
            if maxx[i] < minn[i + 1]:
                temp = (maxx[i] + minn[i + 1]) / 2.0
                minn[i + 1] = (maxx[i] + minn[i + 1]) / 2.0
                maxx[i] = temp
        return  maxx, minn, cent
    
    def tearDown(self):
        '''
        teardown
        @params string featureName:特征名字,number clusters:要聚成几类,string sql:会用到的sql语句
        @retrun
        '''
        self.db.close()