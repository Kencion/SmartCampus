'''
Created on 2017年7月22日
学生画像数据提取模块
在获取训练集和测试集的地方使用
@author: LI
Jack觉得有点乱，建议修改一下
'''
from background_program.b_SampleProcessing.Student import Student
from background_program.z_Tools import MyDataBase
from numpy import mat
import numpy as np

class DataCarer():
    
    def __init__(self, label_name, school_year, usage="regression"):
        '''
                        xxxx
        @params label:xxx
        @return 
        '''
        self.usages = ["regression", "classify"]
        self.usage = usage
        if usage not in self.usages:
            print('用法错误：%s' % usage)
        if usage == "regression":
            self.table_name = "students"
        elif usage == "classify":
            self.table_name = "students_rank"
        
        self.label_name = label_name
        self.school_year = school_year

    def create_train_dataSet(self):
        '''
                        获取训练数据
        @params label:标签列的列名
        @return numpy.mat X_train:特征,numpy.mat Y_train:标签
        '''
        """确定label是哪一列，并将其作为待预测对象"""
        self.open_database()
        self.executer.execute("DESCRIBE {0}".format(self.table_name))
        columnName = self.executer.fetchall()
        index = -1
        for i in range(len(columnName)):
            if str(columnName[i][0]) == self.label_name :
                index = i
                break
        if index == -1:
            print('异常：未发现' + self.label_name)
           
        """先获得数据库表中的全部学生的数据"""
        self.executer.execute("select * from {0}".format(self.table_name))
        dataSet = []
        for i in self.executer.fetchall():
            student = Student(student_num=i[0], features=list(i[1:index]) + list(i[index + 1:]), label=i[index])
            dataSet.append(student.getAll())
        dataSet = np.array(dataSet)
        self.close_database()
        
        dataSet = mat(dataSet)
    
        X_train, Y_train = mat(dataSet[:, :-1]), mat(dataSet[:, -1])
        self.pre_process(X_train)
        return X_train, Y_train
        
    def create_validate_dataSet(self):
        '''
                        获取测试数据
        @params str column:设置把那一列当成结果来预测,str year:学年
        @return list[Student] students:学生列表,numpy.mat X_test:特征
        '''
        """确定label是哪一列，并将其作为待预测对象"""
        self.open_database()
        self.executer.execute("DESCRIBE {0}".format(self.table_name))
        columnName = self.executer.fetchall()
        index = -1
        for i in range(len(columnName)):
            if str(columnName[i][0]) == self.label_name :
                index = i
                break
        if index == -1:
            print('异常：未发现' + self.label_name)
            
        """获得所有学生的数据"""
        sql = "select * from {0} where right(student_num,4) in('{1}','2017')"
        self.executer.execute(sql.format(self.table_name, self.school_year))
        students, X_test = [], []
        for i in self.executer.fetchall():
            student = Student(student_num=i[0], features=list(i[1:index]) + list(i[index + 1:]), label=i[index])
            X_test.append(student.features)
            students.append(student)
        X_test = mat(X_test)
        self.close_database()
        self.pre_process(X_test)
        return students, X_test

    def open_database(self):
        self.db = MyDataBase.MyDataBase("软件学院")
        self.executer = self.db.getExcuter()
        
    def close_database(self):
        self.executer.close()
        self.db.close()
        
    def pre_process(self, X):
        from background_program.b_SampleProcessing.PreProcessing.MyImputer import MyImputer
        
        MyImputer().transformer.fit_transform(X)
        pass