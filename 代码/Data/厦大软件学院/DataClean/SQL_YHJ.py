'''
Created on 2017年11月22日

@author: LENOVO
'''
import pymysql.cursors
import time
from datetime import date, datetime
from boto.sdb.db.sequence import double
conn=pymysql.connect(
                host='172.16.20.5',
                user='root',
                password='',
                db='软件学院',
                charset='utf8mb4'
                )
try:
    #获取会话指针
     with conn.cursor() as cursor:
#生成主键：学号+学年，student_num,student_name,grade,student_type
        sql="select distinct student_num,student_name,grade,student_type from subsidy"
        cursor.execute(sql)
        result=cursor.fetchall()
         #print(result)
        for re in result:
            count=int(re[2])
            if str(re[3])=='普通高校本科学生':
                while count<=int(re[2])+3 & count<=2017:
                    sql="insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                    cursor.execute(sql,(str(re[0])+str(count),re[1],str(re[2]),re[3]))
                    count=count+1
            else:
                while count<=int(re[2])+2 & count<=2017:
                    sql="insert into students(student_num,student_name,student_grade,student_type) values(%s,%s,%s,%s)"
                    cursor.execute(sql,(str(re[0])+str(count),re[1],str(re[2]),re[3]))
                    count=count+1


#score表：导入字段 学年
        sql="select DISTINCT stu_num,left(school_year, 9) from score"
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        for re in result:
            str(re[1]).split('/')
            sql="update students set school_year=%s where student_num=%s"
            #print(re[0],re[1],re[2],re[3])
            cursor.execute(sql,(re[1],str(re[0])+re[1][0:4]))
            #print(str(re[0])+re[1][0:4])
           #cursor.execute(sql)
        #sql="update students set activity_last_time=%s where student_num=%s and school_year=%s"
        conn.commit()


#stu_in_activities导入活动持续总时间
        sql="update students set activity_last_time=%s"
        cursor.execute(sql,double(0))
       #update students set avg_hornorary_times=0;
       #update students set hornorary_amount=0;
        sql="select Distinct Stu_num,DATE_FORMAT(Start_time, '%Y-%m'),sum(time_to_sec(timediff(Finish_time,Start_time))) from stu_in_activities group by stu_num,DATE_FORMAT(Start_time, '%Y-%m')"
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        for re in result:
            re[1].split('-')
            if int(re[1][6:7])<9:
                sql="update students set activity_last_time=%s where student_num=%s"
                cursor.execute(sql,(double(re[2]),str(re[0])+(str)(int(re[1][0:4])-1)))
                #print(((str)(re[1][0:4])))
            else:
                sql="update students set activity_last_time=%s where student_num=%s "
                cursor.execute(sql,(double(re[2]),str(re[0])+(str)(re[1][0:4])))
                #print((str)(re[1][0:4])+'/'+((str)((int)(re[1][0:4])+1)))
        conn.commit()



#hornorary_title导入表彰级别，获奖次数（每学年），获奖总金额
#             sql="select student_num,sum(amount) as amount,grant_year,count(*) as times from hornorary_title where title_name!="" group by student_num,grant_year"
#             cursor.execute(sql)
#             result=cursor.fetchall()
#              #print(result)
#             for re in result:
#                 sql="update students set hornorary_amount=%s,avg_hornorary_times=%s where student_num=%s and school_year=%s"
#                   #sql="update students set hornorary_amount=%s,avg_hornorary_times=%s where student_num=%s and school_year=%s"
#                 cursor.execute(sql,(int(re[1]),int(re[3]),re[0],re[2]))
#                   #print(re[1])
#                   #cursor.execute(sql,(re[0],re[1],re[2],re[3],int(count)))
#             conn.commit()


#library_borrow导入borrow_times每学年借阅总次数
        sql="select student_num,DATE_FORMAT(borrow_date, '%Y-%m'),count(*) from library_borrow group by student_num,DATE_FORMAT(borrow_date, '%Y-%m')"
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        sql="update students set borrow_times=0"
        cursor.execute(sql)
        for re in result:
            re[1].split('-')
            if int(re[1][5:7])<9:
                sql="update students set borrow_times=%s where student_num=%s"
                cursor.execute(sql,(double(re[2]),str(re[0])+(str)(int(re[1][0:4])-1)))
                #print((str)(int(re[1][0:4])-1)+'/'+((str)(re[1][0:4])))
            else:
                sql="update students set borrow_times=%s where student_num=%s"
                cursor.execute(sql,(double(re[2]),str(re[0])+(str)(re[1][0:4])))
                #print((str)(re[1][0:4])+'/'+((str)((int)(re[1][0:4])+1)))
         
            #sql="update students set borrow_times=%s where student_num=%s and school_year=%s"
            #cursor.execute(sql,(int(re[2]),re[0],re[1]))
        conn.commit()
finally:
    conn.close()