'''
Created on 2017年11月22日

@author: yzh
'''

'''
实现将数据库表social_practice中原来无法处理的队员一列分离开来，插入到原来表中。
'''
import pymysql 

db = pymysql.connect("172.16.20.5", "root", "", "软件学院", charset='utf8')
cur = db.cursor()
print("connect ok")
sql = "select team_members,practice_name,start_time,finish_time,practice_place,Keywords,Introduction,School_key_projects_or_not,College_key_projects_or_not,Serial_num from social_practice"
cur.execute(sql)
e = cur.fetchall()
for i in e:
    practice_name = str(i[1])
    start_time = str(i[2])
    finish_time = str(i[3])
    practice_place = str(i[4])
    Keywords = str(i[5])
    Introduction = str(i[6])
    School_key_projects_or_not = str(i[7])
    College_key_projects_or_not = str(i[8])
    Serial_num = str(i[9])
    List = i[0].split(')')
    length = len(List)
    for j in range(length - 1):
        part = List[j].split('(')
        if(str(part[0])[:1]=='\n'):     #考虑到原来数据库中存在换行符的情况。
            stu_name = str(part[0])[1:]
        else:
            stu_name = str(part[0])
        info = part[1].split(', ')
        stu_num = str(info[0])
        college = str(info[1])
        stu_type = str(info[2])
        #print(stu_name)
        #print(stu_num)
        #print(college)
        #print(stu_type)
        sql = "insert into social_practice values('"+Serial_num+"','"+stu_num+"','"+stu_name+"','"+stu_type+"','"+college+"','402','402','"+practice_name+"','"+start_time+"','"+finish_time+"','"+practice_place+"','"+Keywords+"','"+Introduction+"','"+School_key_projects_or_not+"','"+College_key_projects_or_not+"','402','0')"
        #print(sql)
        cur.execute(sql)
db.commit()
print("ok")