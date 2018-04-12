'''
Created on 2018年3月24日

@author: LI
'''
import code

class BeeGroup():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.code=[] #函数的维度，有几个特征就有几个值
        self.trueFit=float(0)#记录真实的最小值
        self.fitness=float(0)
        self.rfitness=float(0)#相对适应值比例
        self.trail=0 #表示实验的次数，用于与limit作比较
        
    def setcode(self,xcode):
        self.code.clear()
        self.code=xcode.copy()
    
    def getcode(self):
        return self.code.copy()
    
    def settrueFit(self,xtrueFit): 
        self.trueFit=xtrueFit
    
    def gettrueFit(self):
        return self.trueFit
    
    def setfitness(self,xfitness):
        self.fitness=xfitness
    
    def getfitness(self):
        return self.fitness
    
    def setrfitness(self,xrfitness):
        self.rfitness=xrfitness
    
    def getrfitness(self):
        return self.rfitness
    
    def settrail(self,xtrail):
        self.trail=xtrail
    
    def gettrail(self):
        return self.trail   
        
    def getAllinof(self):
        result=[]
        result.append(self.getcode())
        result.append(self.getfitness())
        result.append(self.getrfitness())
        result.append(self.gettrail())
        result.append(self.gettrueFit())
        return result