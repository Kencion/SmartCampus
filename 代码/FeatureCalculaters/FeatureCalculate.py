'''
Created on 2017年11月21日
  
@author: jack
'''
 
# 下面是只要执行一次的
from FeatureCalculaters.activities import *
from FeatureCalculaters.dorm_entrance import *
from FeatureCalculaters.hornorary_title import *
from FeatureCalculaters.library import *
from FeatureCalculaters.scholarship import *
from FeatureCalculaters.score import *
from FeatureCalculaters.social_practice import *
from FeatureCalculaters.subsidy import *
from FeatureCalculaters.hornorary_title import *
from tqdm import tqdm

  
from Tools import MyDataBase
db = MyDataBase.MyDataBase("软件学院")
conn = db.getConn()
executer = db.getExcuter()
 
students = list()
sql = "select student_num from students"
executer.execute(sql)
student_nums = executer.fetchall()
db.close()

claculaters = [  
#     activity_avg_level1.activity_avg_level1(),
#     activity_last_time1.activity_last_time1(),
#     activity_num1.activity_num1(),
#     participation_avg_point1.participation_avg_point1(),
#     hornorary_title1.hornorary_title1(), 
#     library_borrow_times1.library_borrow_times1(),
#     library_entrance1.library_entrance1(), 
#     failed_num1.failed_num1(),
#     GPA1.GPA1(),
#     score_rank1.score_rank1(),
#     score1.score1(),
#     is_social_practice_great1.is_social_practice_great1(),
#     social_practice1.social_practice1(),
         
    ]
     
for claculater in tqdm(claculaters):
#     claculater.calculate()
    claculater.cluster()
          
# 关闭数据库
for claculater in tqdm(claculaters):
    claculater.afterCalculate()

# # 下面是要执行学生个数次数的
# claculaters = [
#     library_study_time.library_study_time(),
#     library_week_study_time.library_week_study_time(),
#     scholarship_amount.scholarship_amount(),
#     scholarship_rank.scholarship_rank(),
#     subsidy_amount.subsidy_amount(),
#     subsidy_rank.subsidy_rank(),
#     hornorary_times.hornorary_times(),
#     in_out_times.in_out_times(),
#     hornorary_rank.hornorary_rank(),
#     ]
#    
# for student in student_nums:
#     students.append(student[0][:-4])
#        
# students = set(students)
#   
# for student in tqdm(students):
#     for claculater in claculaters:
#         claculater.setStudentNum(student)
#         claculater.calculate()
#         
# # 关闭数据库
# for claculater in tqdm(claculaters):
#     claculater.afterCalculate()
