'''
Created on 2017年11月23日

@author: LI
'''
from z_Tools import MyDataBase
from tqdm import tqdm
import re 
import os


db = MyDataBase.MyDataBase("软件学院")
executer = db.getExcuter()
sql = "SELECT student_num,grant_year,subsidy_name,amount,rank,subsidy_source FROM `subsidy` where grant_year <>'';"
executer.execute(sql)
result = executer.fetchall()
 
# 将同一个学生获得奖学金的记录进行拆分
for oneResult in tqdm(result):
    YearList = oneResult[1].split('学年')
    for i in range(len(YearList)-1):
        YearList[i]=YearList[i]+'学年'
    
    #拆分奖学金名称,两次分割,分隔符分别为'补助'和'金'    
    NameList =[]
    firstStepList = oneResult[2].split('补助')
    secondStepList=[]
    
    for i in range(len(firstStepList)):
        firstStepList[i] =firstStepList[i] +'补助'
        secondStepList.append(firstStepList[i])
    
    for i in range(len(secondStepList)):
        bufferList =secondStepList[i].split('金')
        for j in range(len(bufferList)):
            if len(bufferList[j])>2 and (len(re.findall(r'.*补助', bufferList[j]))==0):
                bufferList[j]= bufferList[j]+'金'
            if len(bufferList[j])>2:
                NameList.append(bufferList[j])
         
    RankList = re.split(r'等级|等',oneResult[4])
    for i in range(len(RankList)-1):
        RankList[i] = RankList[i]+'等'
        
   
    SourceList = oneResult[5].split('资助')
    for i in range(len(SourceList)-1):
        SourceList[i]=SourceList[i]+'资助'
    #将金额拆分开
    AmountList=[]
    index = 0
    while index < len(oneResult[3]):
#         print(str(index))
        moneystr =''
        while index<len(oneResult[3]):
            moneystr=moneystr+oneResult[3][index]
            if index==(len(oneResult[3])-1):
                index=index+1  
                break
            if oneResult[3][index]=='0' and  oneResult[3][index+1] !='0':
                index =index+1
                break
            index = index+1
        if moneystr !='':
            AmountList.append(moneystr)

    for i in range(len(YearList)-1):
        sql="insert into subsidy_handled values('"+oneResult[0]+"','"+YearList[i]+"','"+NameList[i]\
            +"','"+AmountList[i]\
            +"','"+RankList[i]\
            +"','"+SourceList[i]+"');"
        print(sql)
        executer.execute(sql)    
    
db.close