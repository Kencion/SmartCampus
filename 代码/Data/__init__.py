from Tools import MyDataBase

db = MyDataBase.MyDataBase("软件学院")
executer = db.getExcuter()
sql = "SELECT student_num,grant_year,title_name,title_rank FROM `hornorary_title` where grant_year <>'';"
executer.execute(sql)
result = executer.fetchall()

# 将同一个学生获得荣誉称号的记录进行拆分
for oneResult in result:
    YearList = oneResult[1].split('学年')
    #TitleNameList = oneResult[2].split()
    TitleRankList = oneResult[3].split('级')
    length = len(YearList)
    for i in range(length-1):
        sql  = "insert into hornorary_handled values('"+oneResult[0]+"','"+YearList[i]+"','"+TitleRankList[i]+"级');";
        executer.execute(sql)
        #print(oneResult[0]+'_'+YearList[i]+'__'+TitleRankList[i])
    #print(oneResult)
    

db.close
