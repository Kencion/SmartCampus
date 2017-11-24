'''
Created on 2017年11月21日

@author: 95679
'''
import pymysql 
from builtins import str

db = pymysql.connect("172.16.20.5", "root", "", "软件学院", charset='utf8')
cur = db.cursor()
print("connect ok")
temp = 0
sql = "select distinct(stu_num),grade from score"
cur.execute(sql)
e = cur.fetchall()
for i in e:
#     print(str(i[0]))
    stu_num = str(i[0])
    grade = int(i[1])
    for year in range(grade,2016):
        score1 = 0
        credit1 = 0
        score2 = 0
        credit2 = 0
        score = 0
        year1 = str(year)+'/'+str(year+1)+'-1'
        year2 = str(year)+'/'+str(year+1)+'-2'
        sql = "select score,course_credit from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"   
#         print(sql)
        cur.execute(sql)
        stu1 = cur.fetchone()
#         print(stu1)
        if stu1 is not None:
            score1 = float(stu1[0])
            credit1 = int(stu1[1])
        sql = "select score,course_credit from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"  
#         print(sql)
        cur.execute(sql)
        stu2 = cur.fetchone()
#         print(stu2)
        if stu2 is not None:
            score2 = float(stu2[0])
            credit2 = int(stu2[1])
        if((credit1+credit2)!=0):
            score = (score1*credit1+score2*credit2)/(credit1+credit2)
            sql = "update students set score = "+str(score)+" where student_num = '"+stu_num+str(year)+"'"
            cur.execute(sql)
            temp =temp+1
        else:
            print("err!")
            print(stu_num)
db.commit()        
db.close()
print(temp)
print("ok")
