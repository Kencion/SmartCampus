'''
Created on 2017年7月22日
学生画像数据提取模块
在获取训练集和测试集的地方使用
@author: LI
Jack:建议写成一个类，比较帅
'''
import random
from sklearn.neighbors import NearestNeighbors
from b_SampleProcessing.Student  import Student
from z_Tools import MyDataBase
from numpy import mat
# import Tools.Random_Data as rd
# import pymysql.cursors
# import time
# from datetime import date, datetime
# from boto.sdb.db.sequence import double
# from Tools.Random_Data import  Random_Data

def createTrainDataSet():
    '''
            获取训练数据
    '''
    import numpy as np
    from b_SampleProcessing.PreProcessing.Data_Imbalance_Processing import Data_Imbalance_Processing
    
    db = MyDataBase.MyDataBase("软件学院")
    conn, executer = db.getConn(), db.getExcuter()
    
    a = np.array([[]])  # 没有用的数据，单纯生成对象参数
    dip = Data_Imbalance_Processing(a, N=100)
    lists, proportion = dip._get_proportion('score')  # 分类属性
    new_dataSet = dip._get_data(lists, proportion, 'score')
    
    print(1)
    
    # get all the students
    executer.execute("select * from students_rank")
    dataSet = []
    for i in executer.fetchall():
        student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
        dataSet.append(student.getAll())
    dataSet = np.array(dataSet)
    dataSet += new_dataSet
    dataSet = dataSet.astype('float64')  
         
    conn.close();executer.close()
     
    dataSet = mat(dataSet)
    return mat(dataSet[:, :-1]), mat(dataSet[:, -1])
  
def createValidateDataSet(column='score', year='2016'):
    '''
    get validate data
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
      
                  
def saveResult(students, results, filename):
    '''
            保存数据
    '''
    with open('../AccuracyValidation/results/' + filename + '.csv', 'w')as f:
        # 提交到网上要求的第一行
        f.write("studentid,subsidy\n")
        temp = ""
        for student, result in zip(students, results):
            if result == 1:
                temp = 0
            elif result == 2:
                temp = 1000
            elif result == 3:
                temp = 1500
            elif result == 4:
                temp = 2000
            else:
                print("it is weird")
                
            f.write(str(student.getStudentId()) + "," + str(temp) + "\n")

# def get_train_data_and_test_data():
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
