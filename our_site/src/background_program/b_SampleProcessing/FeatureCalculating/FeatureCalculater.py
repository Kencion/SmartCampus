'''
@author: jack
'''
from background_program.z_Tools import MyLogger

 
class FeatureCalculater:
    '''
            特征计算器的父类
    '''

    def __init__(self, database="软件学院", feature_name=None):
        from background_program.z_Tools import MyDataBase
        
        self.db = MyDataBase.MyDataBase(database)
        self.executer = self.db.getExcuter()
        self.feature_name = feature_name
        self.school_year = ['2013', '2014', '2015', '2016', '2017', ]  # 一个同学一个学年作为一个记录
                 
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
     
    @MyLogger.myException
    def cluster(self, feature_min=None, feature_max=None , clusters=1):
        from sklearn.cluster import KMeans
        import numpy
        '''
                        所有子类都要实现这个函数
                        对特征值进行聚类来归一化处理
        @params 
        @retrun
        '''
        # 获得学生的数据
        sql = 'SELECT {0} FROM 软件学院脱敏.students WHERE {1} is not null and {2} <> 0'.format(self.feature_name, self.feature_name, self.feature_name)
        count = self.executer.execute(sql)
        result = self.executer.fetchall()  # count是行数
        dataSet = numpy.array([i[0] for i in result]).reshape(count, 1)
        
        # 聚类
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(dataSet)  
        center = kmeans.cluster_centers_  # 求出聚类中心
        center_x = ['%0.4f' % center[i][0] for i in range(len(center))]
        labels = kmeans.labels_  # 标注每个点的聚类结果
        
        # 写入student_rank表
        types, maxx, minn = [[] for i in range(0, clusters)], [], []
        for i in range(len(labels)):
            types[labels[i]].append(dataSet[i][0])
            sql = 'select student_num from 软件学院脱敏.students where {0}={1}'.format(self.feature_name, str((dataSet[i][0])))
            self.executer.execute(sql)
            student_nums = self.executer.fetchall()
            for student_num in student_nums:
                student_num = student_num[0]
                sql = "update 软件学院脱敏.students_rank set {0} = {1} where student_num = {2}".format(self.feature_name, str(labels[i] + 1), student_num) 
                n_update = self.executer.execute(sql)
                if n_update == 0:
                    try:
                        sql = 'insert into 软件学院脱敏.students_rank(student_num) values({0})'.format(student_num)
                        self.executer.execute(sql)
                    except:
                        pass
                    sql = "update 软件学院脱敏.students_rank set {0} = {1} where student_num = {2}".format(self.feature_name, str(labels[i] + 1), student_num) 
                    self.executer.execute(sql)
        
        # xxxxxx
        if feature_max is None and feature_min is None:
            for i in range(0, clusters):
                maxx.append(max(types[i]))
                minn.append(min(types[i]))
            maxx, minn, cent = sorted(maxx) , sorted(minn), sorted([float(i) for i in center_x])
            for i in range(len(maxx) - 1):
                if maxx[i] < minn[i + 1]:
                    temp = (float(maxx[i]) + float(minn[i + 1])) / 2.0
                    minn[i + 1] = (float(maxx[i]) + float(minn[i + 1])) / 2.0
                    maxx[i] = temp
            
            sql = 'SELECT max({0}) FROM students'.format(self.feature_name)
            self.executer.execute(sql)
            max_num = int(self.executer.fetchone()[0])
            maxx[len(maxx) - 1] = max_num
        else:
            maxx, minn, cent = feature_max, feature_min, (feature_max + feature_min) / 2.0

        # 将聚类范围保存
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write("activity_avg_level字段" + '\n')
            f.write(str(0) + ':' + str(0) + ' ' + str(0) + ' ' + str(minn[0]) + '\n')  # 手动加入第一区间
            for i in range(len(cent)):
                f.write(str(i + 1) + ':' + str(cent[i]) + ' ' + str(minn[i]) + ' ' + str(maxx[i]) + '\n')
    
    def tearDown(self):
        '''
        teardown
        @params 
        @retrun
        '''
        self.db.close()
