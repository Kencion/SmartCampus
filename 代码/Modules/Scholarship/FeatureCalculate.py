'''
Created on 2017年11月21日
  
@author: jack
'''
 
# 下面是只要执行一次的
from FeatureCalculaters.activities import activity_last_time1
from FeatureCalculaters.hornorary_title import hornorary_title1
from FeatureCalculaters.library import *
from FeatureCalculaters.score import *
from tqdm import tqdm
  
# claculaters = [  
#     activity_last_time1.activity_last_time1(),
#     hornorary_title1.hornorary_title1(),
#     library_borrow1.library_borrow1(),
#     library_entrance1.library_entrance1(),
#     GPA1.GPA1(),
#     score1.score1(),
#     score_rank1.score_rank1(),
#     ]
#    
# for claculater in tqdm(claculaters):
#     claculater.calculate()
#         
# # 关闭数据库
# for claculater in tqdm(claculaters):
#     claculater.afterCalculate()
 
 
from FeatureCalculaters.library import * 
from FeatureCalculaters.scholarship import *
from FeatureCalculaters.subsidy import *
from FeatureCalculaters.hornorary_title import *
from FeatureCalculaters.dorm_entrance import *
  
claculaters = [
    library_study_time.library_study_time(),
    library_week_study_time.library_week_study_time(),
    scholarship_amount.scholarship_amount(),
    scholarship_rank.scholarship_rank(),
    subsidy_amount.subsidy_amount(),
    subsidy_rank.subsidy_rank(),
    hornorary_times.hornorary_times(),
    in_out_times.in_out_times(),
    hornorary_rank.hornorary_rank(),
    ]
  
from Tools import MyDataBase
db = MyDataBase.MyDataBase("软件学院")
conn = db.getConn()
executer = db.getExcuter()
 
students = list()
sql = "select student_num from students"
executer.execute(sql)
student_nums = executer.fetchall()
db.close()
 
for student in student_nums:
    students.append(student[0][:-4])
     
students = set(students)
 
for student in tqdm(students):
    for claculater in claculaters:
        claculater.setStudentNum(student)
        claculater.calculate()
       
# 关闭数据库
for claculater in tqdm(claculaters):
    claculater.afterCalculate()
