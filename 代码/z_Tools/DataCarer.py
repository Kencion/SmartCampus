'''
Created on 2017年7月22日
学生画像数据提取模块
在获取训练集和测试集的地方使用
@author: LI
Jack:建议写成一个类，比较帅
'''
from b_SampleProcessing.Student  import Student
from z_Tools import MyDataBase
from numpy import mat
 
def createTrainDataSet():
    '''
            获取训练数据
    @params 
    @return numpy.mat X_train:特征,numpy.mat Y_train:标签
    '''
    import numpy as np
    from b_SampleProcessing.PreProcessing.Data_Imbalance_Processing import Data_Imbalance_Processing
     
    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()
     
    # 先获得数据库表中的全部学生的数据
    executer.execute("select * from students_rank")
    dataSet = []
    for i in executer.fetchall():
        student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
        dataSet.append(student.getAll())
    executer.close()
    dataSet = np.array(dataSet)
     
    # 获得一些新的数据
    a = np.array([[]])  # 没有用的数据，单纯生成对象参数
    dip = Data_Imbalance_Processing(a, N=100)
    lists, proportion = dip._get_proportion('score')  # 分类属性
    new_dataSet = np.array(list(dip._get_data(lists, proportion, 'score')))
    
    # 把他们加在一起以平衡数据
    print(new_dataSet.shape)
    print(dataSet.shape)
    dataSet=np.vstack((dataSet,new_dataSet))
     
    dataSet = mat(dataSet)
    X_train, Y_train = mat(dataSet[:, :-1]), mat(dataSet[:, -1])
    return X_train, Y_train
   
def createValidateDataSet(column='score', year='2016'):
    '''
            获取测试数据
    @params 
    @return list[Student] students:学生列表,numpy.mat X_test:特征
    '''
    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()
     
    # get all the students
    sql = "select * from students_rank where {0} =0 and right(student_num,4) in('{1}','2017')"
    executer.execute(sql.format(column, year))
    students, dataSet = [], []
    for i in executer.fetchall():
        student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
        dataSet.append(student.getAll())
        students.append(student)
         
    executer.close()
     
    dataSet = mat(dataSet)
     
    return students, dataSet[:, :-1]
                   
# def get_train_data_and_test_data():
#     import random
#     from sklearn.neighbors import NearestNeighbors
    # import Tools.Random_Data as rd
    # import pymysql.cursors
    # import time
    # from datetime import date, datetime
    # from boto.sdb.db.sequence import double
    # from Tools.Random_Data import  Random_Data
#     #从数据库提取特征属性
#     sql="select subsidy_amount,scholarship_amount from students where subsidy_amount!=0 and scholarship_amount!=0"
#     cursor.execute(sql)
#     result=cursor.fetchall()
#     #从数据库获取分类标签
#     sql="select distinct(scholarship_amount) from students"
#     cursor.execute(sql)
#     label=cursor.fetchall()
#     #获取训练集和验证集
#     rd.Random_Data.group(result, label, 0.1)