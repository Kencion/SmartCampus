'''
Created on 2018年3月24日

@author: LI
'''
import random as RD
import BeeGroup as BG
import math

def random(xlb,xub):
    '''
        产生区间上的随机数
    xlb为下界
    xrb为上界
    '''
    
    return RD.uniform(xlb,xub)

def initilize(xFoodNumber,xD,xlb,xub):
    '''
        初始化参数
    '''
    NectarSource=[]#蜜源，注意：一切的修改都是针对蜜源而言的 
    EmployedBee=[]#采蜜蜂
    OnLooker=[]#观察蜂
    BestSource =BG.BeeGroup()#记录最好蜜源

    for i in range(0,int(xFoodNumber)):
        NectarSource.append(BG.BeeGroup())
        EmployedBee.append(BG.BeeGroup())
        OnLooker.append(BG.BeeGroup())
        code=[]
        for j in range(0,xD):
            code.append(random(xlb,xub))
        NectarSource[i].setcode(code) 
        EmployedBee[i].setcode(code) 
        OnLooker[i].setcode(code)
        BestSource.setcode(code)
        
        #蜜源初始化
        NectarSource[i].settrueFit(calculationTruefit(NectarSource[i]))
        NectarSource[i].setfitness(calculationFitness(NectarSource[i].gettrueFit())) 
        NectarSource[i].setrfitness(0)
        NectarSource[i].settrail(0)
        
        #采蜜蜂初始化
        EmployedBee[i].settrueFit(NectarSource[i].gettrueFit())
        EmployedBee[i].setfitness(NectarSource[i].getfitness())  
        EmployedBee[i].setrfitness(NectarSource[i].getrfitness())  
        EmployedBee[i].settrail(NectarSource[i].gettrail())
        
        #观察蜂初始化
        OnLooker[i].settrueFit(NectarSource[i].gettrueFit())
        OnLooker[i].setfitness(NectarSource[i].getfitness()) 
        OnLooker[i].setrfitness(NectarSource[i].getrfitness()) 
        OnLooker[i].settrail(NectarSource[i].gettrail())
        
        code.clear()
        
    #最优蜜源初始化
    BestSource.settrueFit(NectarSource[0].gettrueFit())  
    BestSource.setfitness(NectarSource[0].getfitness())  
    BestSource.setrfitness(NectarSource[0].getrfitness())  
    BestSource.settrail(NectarSource[0].gettrail()) 
    
    return NectarSource,EmployedBee,OnLooker,BestSource

def calculationTruefit(xbee):
    '''
        计算真实的函数值
    '''
    truefit=0.5+(math.sin(math.sqrt(xbee.code[0]*xbee.code[0]+xbee.code[1]*xbee.code[1]))*math.sin(math.sqrt(xbee.code[0]*xbee.code[0]+xbee.code[1]*xbee.code[1]))-0.5)\
    /((1+0.001*(xbee.code[0]*xbee.code[0]+xbee.code[1]*xbee.code[1]))*(1+0.001*(xbee.code[0]*xbee.code[0]+xbee.code[1]*xbee.code[1])));  
  
    return truefit;  

def calculationFitness(xtruefit):
    '''
        计算适应值
    '''
    fitnessResult=float(0)  
    if xtruefit>=0:  
        fitnessResult=1/float((xtruefit+1))
    else:  
        fitnessResult=1-xtruefit 
      
    return fitnessResult

def calculateProbabilities(xFoodNumber,xNectarSource):
    '''
        计算轮盘赌的概率
    ''' 
    maxfit=xNectarSource[0].getfitness()  
    for i in range(1,int(xFoodNumber)) :   
        if xNectarSource[i].getfitness()>maxfit:  
            maxfit=xNectarSource[i].getfitness()  
    
      
    for i in range(0,int(xFoodNumber)) : 
        xNectarSource[i].setrfitness((0.9*(xNectarSource[i].getfitness()/maxfit))+0.1)  
    
    return xNectarSource

def evalueSource():
    '''
        评价蜜源
    '''
    pass

def sendEmployedBees(xFoodNumber,xD,xNectarSource,xEmployedBee,xlb,xub):
    for i in range(0,int(xFoodNumber)):
        param2change=int(random(0,xD))
        
        #选取不等于i的k
        while True:
            k = int(random(0,xFoodNumber))
            if k!=i:
                break
        xEmployedBee[i].setcode(xNectarSource[i].getcode())
        
        #采蜜蜂去更新信息
        Rij = random(-1,1)
        oldcode=xEmployedBee[i].getcode()
        oldcode[param2change]=(xNectarSource[i].getcode())[param2change]+Rij*((xNectarSource[i].getcode())[param2change]-(xNectarSource[k].getcode())[param2change])
        
        #判断是否越界
        if  oldcode[param2change]>xub: 
            oldcode[param2change]=xub
         
        if  oldcode[param2change]<xlb: 
            oldcode[param2change]=xlb
        
        xEmployedBee[i].setcode(oldcode)
          
        xEmployedBee[i].settrueFit(calculationTruefit(xEmployedBee[i]))  
        xEmployedBee[i].setfitness(calculationFitness(xEmployedBee[i].gettrueFit()))
        
        #贪心选择策略
        if xEmployedBee[i].gettrueFit()<xNectarSource[i].gettrueFit():
            xNectarSource[i].setcode(xEmployedBee[i].getcode())
            xNectarSource[i].settrail(0);  
            xNectarSource[i].settrueFit(xEmployedBee[i].gettrueFit())  
            xNectarSource[i].setfitness(xEmployedBee[i].getfitness())
                   
        else :
            xNectarSource[i].settrail(xNectarSource[i].gettrail()+1)
        
    return xNectarSource,xEmployedBee

def sendOnlookerBees(xFoodNumber,xD,xNectarSource,xOnLooker,xlb,xub):
    '''
        观察蜂与采蜜蜂交流信息，采蜜蜂更改信息
    '''
    i=0
    t=0  
    while t<int(xFoodNumber) :      
        R_choosed=random(0,1) #被选中的概率  
        if R_choosed<xNectarSource[i].getrfitness() :#根据被选择的概率选择            
            t=t+1 
            param2change=int(random(0,xD))#需要被改变的维数  
              
            #选取不等于i的k
            while True :   
                k=int(random(0,xFoodNumber))
                if k!=i:   
                    break
     
            xOnLooker[i].setcode(xNectarSource[i].getcode())
            #更新 
            Rij = random(-1,1)
            oldcode=xOnLooker[i].getcode()
            oldcode[param2change]=(xNectarSource[i].getcode())[param2change]+Rij*((xNectarSource[i].getcode())[param2change]-(xNectarSource[k].getcode())[param2change])
            
            #判断是否越界
            if  oldcode[param2change]>xub: 
                oldcode[param2change]=xub
             
            if  oldcode[param2change]<xlb: 
                oldcode[param2change]=xlb
            
            xOnLooker[i].setcode(oldcode)
              
            xOnLooker[i].settrueFit(calculationTruefit(xOnLooker[i]))  
            xOnLooker[i].setfitness(calculationFitness(xOnLooker[i].gettrueFit()))
              
            #贪心选择策略
            if xOnLooker[i].gettrueFit()<xNectarSource[i].gettrueFit():
                xNectarSource[i].setcode(xOnLooker[i].getcode())
                xNectarSource[i].settrail(0);  
                xNectarSource[i].settrueFit(xOnLooker[i].gettrueFit())  
                xNectarSource[i].setfitness(xOnLooker[i].getfitness())
                   
            else :
                xNectarSource[i].settrail(xNectarSource[i].gettrail()+1)     
        i=i+1 
        if i==int(xFoodNumber) : 
            i=0
      
    return xNectarSource,xOnLooker

def sendScoutBees(xFoodNumber,xD,xNectarSource,xlb,xub,xlimit):
    '''
        判断是否有侦查蜂的出现，有则重新生成蜜源
    '''
    maxtrialindex=0;  
    for i in range(1,int(xFoodNumber)): 
    
        if xNectarSource[i].gettrail()>xNectarSource[maxtrialindex].gettrail():   
            maxtrialindex=i;    
      
    if xNectarSource[maxtrialindex].gettrail()>=xlimit:  
        #重新初始化 
        code=[]
        for j in range(0,xD):
            R=random(0,1)
            code.append(xlb+R*(xub-xlb))
        xNectarSource[maxtrialindex].setcode(code)  
        xNectarSource[maxtrialindex].settrail(0)  
        xNectarSource[maxtrialindex].settrueFit(calculationTruefit(xNectarSource[maxtrialindex]))  
        xNectarSource[maxtrialindex].setfitness(calculationFitness(xNectarSource[maxtrialindex].gettrueFit()))  
    return xNectarSource

def MemorizeBestSource(xFoodNumber,xNectarSource,xBestSource):
    for i in range(0,int(xFoodNumber)):
        if xNectarSource[i].gettrueFit()<xBestSource.gettrueFit():
            xBestSource.setcode(xNectarSource[i].getcode())
            xBestSource.settrueFit(xNectarSource[i].gettrueFit())
    return xBestSource