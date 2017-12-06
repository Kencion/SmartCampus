'''
Created on 2017年7月22日
学生画像数据提取模块
在获取训练集和测试集的地方使用
@author: LI
Jack:有点乱，建议修改一下
'''
from b_SampleProcessing.Student  import Student
from z_Tools import MyDataBase
from numpy import mat

class DataCarer():
    
    def __init__(self):
        pass
    
    def createTrainDataSet(self):
        '''
                        获取训练数据
        @params 
        @return numpy.mat X_train:特征,numpy.mat Y_train:标签
        '''
        import numpy as np
        from b_SampleProcessing.PreProcessing.Data_Imbalance_Processing import Data_Imbalance_Processing
        from b_SampleProcessing.Datasample_Layering.Random_Data import Random_Data 
         
        db = MyDataBase.MyDataBase("软件学院")
        executer = db.getExcuter()
         
        """先获得数据库表中的全部学生的数据"""
        executer.execute("select * from students_rank")
        dataSet = []
        for i in executer.fetchall():
            student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
            dataSet.append(student.getAll())
        executer.close()
        dataSet = np.array(dataSet)
        
        """获得一些新的数据"""
        a = np.array([[]])  # 没有用的数据，单纯生成对象参数
        dip = Data_Imbalance_Processing(a, N=100)
        lists, proportion = dip._get_proportion('score')  # 分类属性
        new_dataSet = np.array(list(dip._get_data(lists, proportion, 'score')))
        
        """把他们加在一起以平衡数据"""
        try:
            dataSet = np.vstack((dataSet, new_dataSet))
            dataSet = mat(dataSet)
        except:
            pass
         
        """ 对刚才的数据进行分层抽样"""
        X_train, Y_train = mat(dataSet[:, :-1]), mat(dataSet[:, -1])
        X_train=tuple(X_train.tolist())
        t=list()
        for i in range(len(Y_train)):
            t.append(Y_train[i,0])
        Y_train=tuple(set(t))
        
        dataSet, _ = Random_Data().group(data_set=dataSet, label=Y_train, percent=0.1)
        dataSet=mat(dataSet)
 
        X_train, Y_train = mat(dataSet[:, :-1]), mat(dataSet[:, -1])
        
        return X_train, Y_train
       
    def createValidateDataSet(self, column='score', year='2016'):
        '''
                        获取测试数据
        @params str column:设置把那一列当成结果来预测,str year:学年
        @return list[Student] students:学生列表,numpy.mat X_test:特征
        '''
        db = MyDataBase.MyDataBase("软件学院")
        executer = db.getExcuter()
         
        """获得所有学生的数据"""
        sql = "select * from students_rank where  right(student_num,4) in('{0}','2017')"
        executer.execute(sql.format( year))
        students, X_test = [], []
        for i in executer.fetchall():
            student = Student(student_num=i[0], features=list(i[1:-1]), label=i[-1])
            X_test.append(student.features)
            students.append(student)
        executer.close()
        #print(len(X_test))
        X_test = mat(X_test)
        
        return students, X_test
