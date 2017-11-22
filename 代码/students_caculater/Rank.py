'''
Created on 2017年11月22日

@author: 95679
'''
import pymysql 

db = pymysql.connect("172.16.20.5", "root", "", "软件学院", charset='utf8')
cur = db.cursor()
print("connect ok")
sql = "select student_num,school_year from students"
cur.execute(sql)
e = cur.fetchall()
for i in e:
    rank1 = 0
    rank2 = 0
    rank = 0
    stu_num = str(i[0])[:-4]
    school_year = str(i[0])[-4:]
    next_year = str(int(school_year)+1)
    year1 = school_year + "/" +next_year+"-1"
    year2 = school_year + "/" +next_year+"-2"
    sql = "select Rank from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"  
    print(sql)
    cur.execute(sql)
    stu1 = cur.fetchone()
    print(stu1)
    if(stu1!=None):
        rank1 = int(stu1[0])
    sql = "select Rank from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"
    cur.execute(sql)
    stu2 = cur.fetchone()
    if(stu2!=None):
        rank2 = float(stu2[0])
    rank = (rank1+rank2)/2
    print(rank)
    sql = "update students set rank = "+str(rank)+" where student_num = '"+stu_num+school_year+"'"
    cur.execute(sql)
db.close()
print("ok")
