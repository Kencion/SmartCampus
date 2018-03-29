'''
Created on 2018年3月24日

@author: LI
'''
import matplotlib.pyplot as plt
#引用种群的定义
import background_program.z_Tools.featureselect.BeeGroup as BG
import background_program.z_Tools.featureselect.baseFunction as baseFunction
from pylab import *  
import background_program.y_Modules.class_failing_warning as class_failing_warning


class myABC():
    def __init__(self,xNP=40,xlimit=20,xmaxCycle=10000,xD=2,xlb=-100,xub=100):
        '''
        NP 种群的规模，采蜜蜂+观察蜂 
        FoodNumber=NP/2 食物的数量，为采蜜蜂的数量  
        limit 限度，超过这个限度没有更新采蜜蜂变成侦查蜂
        maxCycle 停止条件 
        D=2#函数的参数个数
        lb=-100#函数的下界   
        ub=100#函数的上界 
        '''
        self.NP=xNP
        self.FoodNumber=self.NP/2
        self.limit=xlimit
        self.maxCycle=xmaxCycle
        self.D=xD
        self.lb=xlb
        self.ub=xub
        self.module=None
        self.NectarSource=None
        self.EmployedBee=None
        self.Onlooker=None
        self.BestSource=None
        self.X_train=None
        self.X_validate=None
        
    
    def run(self):
        #主函数
        f= open('process.txt','w')#将迭代过程保存至文件中
        
        self.NectarSource,self.EmployedBee,self.OnLooker,self.BestSource = \
                                        baseFunction.initilize(self.FoodNumber,self.D,self.lb,self.ub,
                                        self.module,self.X_train,self.X_validate) 
        self.BestSource=baseFunction.MemorizeBestSource(self.FoodNumber,self.NectarSource,self.BestSource)
        process=[]
        
        #主要循环
        gen =0
        while gen<self.maxCycle :
            self.NectarSource,self.EmployedBee=\
                                baseFunction.sendEmployedBees(self.FoodNumber,self.D,self.NectarSource,
                                                              self.EmployedBee,self.lb,self.ub,
                                                              self.module,self.X_train,self.X_validate)
            self.NectarSource=baseFunction.calculateProbabilities(self.FoodNumber,self.NectarSource)  
            self.NectarSource,self.OnLooker=\
                                baseFunction.sendOnlookerBees(self.FoodNumber,self.D,self.NectarSource,
                                                              self.OnLooker,self.lb,self.ub,self.module,
                                                              self.X_train,self.X_validate)  
            self.BestSource=baseFunction.MemorizeBestSource(self.FoodNumber,self.NectarSource,self.BestSource) 
            self.NectarSource=\
                                baseFunction.sendScoutBees(self.FoodNumber,self.D,self.NectarSource,
                                                           self.lb,self.ub,self.limit,self.module,
                                                           self.X_train,self.X_validate)  
            self.BestSource=baseFunction.MemorizeBestSource(self.FoodNumber,self.NectarSource,self.BestSource)
           
            f.write(str(self.BestSource.trueFit)) 
            f.write('\n')
            process.append(self.BestSource.trueFit) 
            gen=gen+1
        
        f.close()
        
        mpl.rcParams['font.sans-serif'] = ['SimHei'] #在matplotlib中显示中文
        x=range(1,self.maxCycle+1)
        plt.xlabel('迭代次数')
        plt.ylabel('tureFit')
        plt.plot(x,process)
        plt.show()
        
        
if __name__=='__main__':
    item=myABC()
    testmodule=class_failing_warning.class_failing_warning()
    oldDataset = test.X_train
    D=len(oldDataset[0]) #获取原数据集的特征数，即维度
    item.D=D
    item.module=testmodule
    item.X_train=testmodule.X_train
    item.X_validate=testmodule.X_validate
    item.run()