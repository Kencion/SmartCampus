'''
Created on 2017年11月21日

学生类，要画像的对象

@author: jack
'''
class Student():
    '''
            用户的画像类
    '''
    def __init__(self, student_num, features=None, label="1"):
        self.student_num = student_num
        try:
            self.features = list(features)
        except:
            pass
        self.label = label
        
    def setStudent_num(self, student_num): 
        self.student_num = student_num
    
    def getStudent_num(self):
        return self.student_num
        
    def getAll(self):
        '''
                        返回特征+标签
        '''
        return self.features + [self.label]
    
