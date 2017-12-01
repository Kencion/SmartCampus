'''
Created on 2017年11月21日
@author: jack
'''
class Student():
    '''
              学生类，要画像的对象
    '''
    def __init__(self, student_num, features=None, label="1"):
        self.student_num = student_num
        try:
            self.features = list(features)
        except:
            pass
        self.label = label
        
    def setStudent_num(self, student_num): 
        '''
                        设置学号
        @params string student_num:学生学号
        @retrun
        '''
        self.student_num = student_num
    
    def getStudent_num(self):
        '''
                        获取学号
        @params 
        @retrun string self.student_num:学生学号
        '''
        return self.student_num
        
    def getAll(self):
        '''
                        返回特征+标签
        @params 
        @retrun list[[]] features_and_labels:[特征,标签]
        '''
        features_and_labels=self.features+[self.label]
        return features_and_labels
    
