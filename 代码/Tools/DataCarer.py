'''
Created on 2017年7月22日
学生画像数据提取模块
@author: ljs
'''
from FeatureCalculaters.Student  import Student
from Tools import MyDataBase
import random
from sklearn.neighbors import NearestNeighbors
from numpy import mat

def createTrainDataSet():
    '''
            获取训练数据
    '''
    db = MyDataBase.MyDataBase("软件学院")
    conn, executer = db.getConn(), db.getExcuter()
    
    # get all the students
    executer.execute("select * from students_rank")
    dataSet = []
    for i in executer.fetchall():
        student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
        dataSet.append(student.getAll())
        
    conn.close();executer.close()
    
    dataSet = mat(dataSet)
    return mat(dataSet[:, :-1]), mat(dataSet[:, -1])
  
def createValidateDataSet():
    '''
    get validate data
    '''
    db = MyDataBase.MyDataBase("软件学院")
    conn, executer = db.getConn(), db.getExcuter()
    
    # get all the students
    executer.execute("select * from students_rank")
    students, dataSet = [], []
    for i in executer.fetchall():
        student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
        dataSet.append(student.getAll())
        students.append(student)
        
    conn.close();executer.close()
    
    dataSet = mat(dataSet)
    
    return students, dataSet[:, :-1]
      
def DataImbalanceProcessing(dataSet):
    # 处理数据不平衡问题
    # 统计每种类别的个数
    classCount = {'A':0, 'B':0, 'C':0, 'D':0}
    for i in dataSet:
        classCount[(isinstance(i[-1], int) and str(chr(ord('A') + i[-1] - 1))) or str(i[-1])] += 1
    classCount_result = sorted(classCount.items(), key=lambda asd:asd[1], reverse=False)
    flag = True
    while flag:
        flag = False
        for i in classCount_result[:-1]:
            if i[1] > 0 and 20 * i[1] < classCount_result[-1][1]:
                flag = True
                type = i[0]
                temp = []
                for student in dataSet :
                    if ((isinstance(student[-1], int) and str(chr(ord('A') + student[-1] - 1))) or str(student[-1])) == type:
                        t = student[:]
                        temp.append(t)
                        classCount[type] += 1
                dataSet.extend(temp)
                classCount_result = sorted(classCount.items(), key=lambda asd:asd[1], reverse=False)
                  
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

