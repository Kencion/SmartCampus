'''
Created on 2017年11月22日

@author: 95679
'''

import pymysql 
'''
str = '223201422010482015'
print(str[:-4])
print(str[-4:])
'''

db = pymysql.connect("172.16.20.5", "root", "", "软件学院", charset='utf8')
cur = db.cursor()
print("connect ok")
sql = "select student_num from students"
cur.execute(sql)
e = cur.fetchall()
for i in e:
    num1 = 0
    num2 = 0
    stu_num = str(i[0])[:-4]
    school_year = str(i[0])[-4:]
    next_year = str(int(school_year)+1)
    year1 = school_year + "/" +next_year+"-1"
    year2 = school_year + "/" +next_year+"-2"
    sql = "select substring_index(failed_num,'(',1) from score where stu_num = '"+stu_num+"' and school_year = '"+year1+"'"
    print(sql)
    cur.execute(sql)
    stu1 = cur.fetchone()
    print(stu1)
    if(stu1!=None):
        num1 = float(stu1[0])
    sql = "select substring_index(failed_num,'(',1) from score where stu_num = '"+stu_num+"' and school_year = '"+year2+"'"
    cur.execute(sql)
    stu2 = cur.fetchone()
    if(stu2!=None):
        num2 = float(stu2[0])
    num = num1 + num2
    print(num)
    sql = "update students set failed_num = "+num+" where student_num = '"+stu_num+school_year+"'"
    cur.execute(sql)
db.close()
print("ok")