'''
@author: jack
'''
from Tools import MyDataBase
from Tools import MyLogger
 
class FeatureCalculater:
    '''
            特征计算器的父类
    '''
    def __init__(self, database="软件学院"):
        self.db = MyDataBase.MyDataBase(database)
        self.executer = self.db.getExcuter()
        self.school_year = ['2014', '2015', '2016', '2017', ]  # 一个同学一个学年作为一个记录
        self.level = None
                 
    def setStudentNum(self, student_num):
        self.student_num = student_num
         
    def setLevel(self):
        '''
                        设置等级划分标准
        '''
        pass
     
    @MyLogger.myException
    def calculate(self):
        '''
                        所有子类都要实现这个函数
        '''
        pass  
     
    def classify(self, param):
        '''
                        对结果按等级进行划分
        '''
        if param is None:
            return 0
         
        for i in range(len(self.level)):
            if float(param) <= float(self.level[i]):
                return str(i + 1)
             
        return str(len(self.level) + 1)
     
    def afterCalculate(self):
        self.db.close()
 
if __name__ == '__main__':
    pass
