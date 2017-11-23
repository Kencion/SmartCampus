'''
Created on 2017年11月21日
 
@author: jack
'''

# 下面是只要执行一次的
from FeatureCalculaters.activities import stu_in_activities1
from FeatureCalculaters.hornorary_title import hornorary_title1
from FeatureCalculaters.library import library_borrow1
from FeatureCalculaters.library import library_entrance1
from FeatureCalculaters.score import GPA1
from FeatureCalculaters.score import school_year1
from FeatureCalculaters.score import score1
from FeatureCalculaters.score import score_rank1
#from tqdm import tqdm

claculaters = [#stu_in_activities1.stu_in_activities1(),
#     hornorary_title1.hornorary_title1(),
#     library_borrow1.library_borrow1(),
#     library_entrance1.library_entrance1(),

     GPA1.GPA1(),
    
     #school_year1.school_year1(),
     #score1.score1(),
    #score_rank1.score_rank1(),
    ]
for claculater in claculaters:
    claculater.calculate()
#      
# # 关闭数据库
for claculater in claculaters:
    claculater.afterCalculate()


from FeatureCalculaters.library import * 
from FeatureCalculaters.scholarship import *
from FeatureCalculaters.subsidy import *

claculaters = [library_study_time.library_study_time(),
            library_week_study_time.library_week_study_time(),
            scholarship_amount.scholarship_amount(),
            scholarship_rank.scholarship_rank(),
            subsidy_amount.subsidy_amount(),
            subsidy_rank.subsidy_rank(),
    ]
 
students = []

for student in students:
    for claculater in claculaters:
        claculater.setStudent(student)
        claculater.calculate()
      
# 关闭数据库
for claculater in claculaters:
    claculater.afterCalculate()

