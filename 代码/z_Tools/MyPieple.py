'''
Created on 2017年11月24日

@author: Jack
'''
class MyPieple():
    '''
            管道，可以把每个步骤放进来，这样跑起来很方便
            采用集合模式
    '''
    
    def __init__(self):
        self.sections=[]
    
    def doit(self):
        '''
                        把每个段的doit都调用一次
        @params 
        @retrun
        '''
        for section in self.sections:
            section.doit()
