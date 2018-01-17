'''
@author: jack
'''

from background_program.z_Tools.my_exceptions import my_exception_handler

 
class FeatureCalculater:
    '''
            特征计算器的父类
    '''

    def __init__(self, database="软件学院", feature_name=None):
        from background_program.z_Tools.my_database import MyDataBase
        
        self.db = MyDataBase(database)
        self.executer = self.db.getExcuter()
        self.feature_name = feature_name
        self.this_year = 2017  # 一个同学一个学年作为一个记录
            
    def get_school_year(self, student_num):
        in_year = int(student_num[3:7])
        school_year = [str(i) for i in range(in_year, self.this_year + 1)]
        
        return school_year
         
    @my_exception_handler                 
    def add_student(self, student_num):
        '''
                        添加学生
        @params string student_num:学生学号
        @retrun
        '''
        sql = "insert into students(student_num) values('{0}')".format(student_num)
        self.executer.execute(sql)
         
    @my_exception_handler
    def calculate(self):
        '''
                        获取学号
                        所有子类都要实现这个函数
                        特征值的计算
        @params 
        @retrun
        '''
        sql = "select distinct student_num,student_name,grade,student_type from subsidy"
        self.executer.execute(sql)
        result = self.executer.fetchall()
        student_types = ['普通高校本科学生', '硕士研究生', '交流生', '普通进修生', '硕士专业学位研究生']
        for re in result:
            count = int(re[2])
            for s_i in range(len(student_types)):
                if re[3] == student_types[s_i]:
                    student_type = s_i
                    break
            if student_type == 0:
                while count <= int(re[2]) + 8 and count <= 2017:
                    sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                    self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), student_type))
                    count = count + 1
            else:
                while count <= int(re[2]) + 8 and count <= 2017:
                    sql = "insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                    self.executer.execute(sql, (str(re[0]) + str(count), re[1], str(re[2]), student_type))
                    count = count + 1  
     
    @my_exception_handler
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
        sql = 'SELECT {0} FROM students_float WHERE {1} is not null and {2} <> 0'.format(self.feature_name, self.feature_name, self.feature_name)
        count = self.executer.execute(sql)
        result = self.executer.fetchall()  # count是行数
        dataSet2 = list(result)
        dataSet = numpy.array([i[0] for i in result]).reshape(count, 1)
        
        # 聚类
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(dataSet)  
        center = kmeans.cluster_centers_  # 求出聚类中心
        center_x = ['%0.4f' % center[i][0] for i in range(len(center))]
        labels = kmeans.labels_  # 标注每个点的聚类结果
        # 写入student_rank表
        types, maxx, minn = [[] for i in range(0, clusters)], [], []
        dataSet_quene = list(set(dataSet2))
        print(len(dataSet_quene))
        for i in range(len(labels)):
            types[labels[i]].append(dataSet[i][0])
            if len(dataSet_quene) > 0:
                for j in range(len(dataSet_quene)):
                    if dataSet[i][0] == dataSet_quene[j]:
                        del dataSet_quene[j]
                        print(len(dataSet_quene))
                        sql = 'select student_num from students_float where {0}={1}'.format(self.feature_name, str((dataSet[i][0])))
                        self.executer.execute(sql)
                        student_nums = self.executer.fetchall()
                        for student_num in student_nums:
                            student_num = student_num[0]
                            sql = "update students_int set {0} = {1} where student_num = {2}".format(self.feature_name, str(labels[i] + 1), student_num) 
                            n_update = self.executer.execute(sql)
                            if n_update == 0:
                                try:
                                    sql = 'insert into students_int(student_num) values({0})'.format(student_num)
                                    self.executer.execute(sql)
                                except:
                                    pass
                                sql = "update students_int set {0} = {1} where student_num = {2}".format(self.feature_name, str(labels[i] + 1), student_num) 
                                self.executer.execute(sql)
                        break
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
            
            sql = 'SELECT max({0}) FROM students_float'.format(self.feature_name)
            self.executer.execute(sql)
            max_num = int(self.executer.fetchone()[0])
            maxx[len(maxx) - 1] = max_num
        else:
            maxx, minn, cent = feature_max, feature_min, (feature_max + feature_min) / 2.0  
        # 将聚类范围保存
        with open(r"Cluster_Feature", "a", encoding='utf8') as f:
            f.write(str(self.feature_name) + '\n')
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
