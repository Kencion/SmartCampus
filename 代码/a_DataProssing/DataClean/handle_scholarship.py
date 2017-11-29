'''
Created on 2017年11月23日

@author: LI
'''
from z_Tools import MyDataBase
from tqdm import tqdm


db = MyDataBase.MyDataBase("软件学院")
executer = db.getExcuter()
sql = "SELECT student_num,grant_year,scholarship_name,amount,scholarship_type,scholarship_ratio FROM `scholarship` where grant_year <>'';"
executer.execute(sql)
result = executer.fetchall()
 
# 将同一个学生获得奖学金的记录进行拆分
for oneResult in tqdm(result):
    #拆分学年,可用
    YearList = oneResult[1].split('学年')
    for i in range(len(YearList)):
        YearList[i]=YearList[i]+'学年'
         
    NameList = oneResult[2].split('奖学金')
    for i in range(len(NameList)):
        NameList[i] =NameList[i] +'奖学金'
         
    TypeList = oneResult[4].split('奖学金')
    for i in range(len(TypeList)):
        TypeList[i] = TypeList[i]+'奖学金' 
        
    
    RatioList = oneResult[5].split('1/')
    for i in range(1,len(RatioList)):
        RatioList[i]='1/'+RatioList[i]
        
    #将金额拆分开,可用
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
#             print(moneystr+'__index='+str(index)+'__'+str(len(oneResult[3])))
            AmountList.append(moneystr)
  
    for i in range(len(YearList)-1):
        sql="insert into scholarship_handled values('"+oneResult[0]+"','"+YearList[i]+"','"+NameList[i]\
            +"','"+AmountList[i]+"','"+TypeList[i]+"','"\
            +RatioList[i+1]+"');"
        executer.execute(sql)    
    
db.close