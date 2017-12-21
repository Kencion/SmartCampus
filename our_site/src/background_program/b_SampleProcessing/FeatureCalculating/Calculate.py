'''
Created on 2017年11月21日
  
@author: jack
细化聚类流程
'''
import warnings
warnings.filterwarnings("ignore")
 
# 下面是只要执行一次的
from background_program.b_SampleProcessing.FeatureCalculating.activities import *
# from background_program.b_SampleProcessing.FeatureCalculating.dorm_entrance import *
# from background_program.b_SampleProcessing.FeatureCalculating.hornorary_title import *
# from background_program.b_SampleProcessing.FeatureCalculating.library import *
# from background_program.b_SampleProcessing.FeatureCalculating.scholarship import *
# from background_program.b_SampleProcessing.FeatureCalculating.score import *
# from background_program.b_SampleProcessing.FeatureCalculating.social_practice import *
# from background_program.b_SampleProcessing.FeatureCalculating.subsidy import *
# from background_program.b_SampleProcessing.FeatureCalculating.hornorary_title import *
# from background_program.b_SampleProcessing.FeatureCalculating.card.canteen_consumption_divide_by_consumption import canteen_amount_divide_by_consumption
# from background_program.b_SampleProcessing.FeatureCalculating.card.canteen_times import canteen_times
# from background_program.b_SampleProcessing.FeatureCalculating.card.Consumption import Consumption
# from background_program.b_SampleProcessing.FeatureCalculating.card.max_every_type import max_every_type
# from background_program.b_SampleProcessing.FeatureCalculating.card.mean_median_var import mean_median_var
# from background_program.b_SampleProcessing.FeatureCalculating.card.total_amount_every_type import total_amount_every_type
# from background_program.b_SampleProcessing.FeatureCalculating.card.transaction_times import transaction_times
from tqdm import tqdm  

claculaters1 = [  
#         activity_avg_level1.activity_avg_level1(),
        activity_last_time1.activity_last_time1(),
        activity_num1.activity_num1(),
#         participation_avg_point1.participation_avg_point1(),
#         library_borrow_times1.library_borrow_times1(),
#         library_entrance1.library_entrance1(),
#         failed_num1.failed_num1(),
#         GPA1.GPA1(),
#         score_rank1.score_rank1(),
#         score1.score1(),
#         is_social_practice_great1.is_social_practice_great1(),
#         social_practice1.social_practice1(),
#         hornorary_rank.hornorary_rank(),
#         hornorary_times.hornorary_times(),
#             canteen_times,
#             Consumption,
#             max_every_type,
#             mean_median_var,
#             total_amount_every_type,
#             transaction_times,
#             canteen_amount_divide_by_consumption,
    ]

# 下面是要执行学生个数次数的
claculaters2 = [
#     library_study_time.library_study_time(),
#     library_week_study_time.library_week_study_time(),
#     scholarship_amount.scholarship_amount(),
#     scholarship_rank.scholarship_rank(),
#     subsidy_amount.subsidy_amount(),
#     subsidy_rank.subsidy_rank(),
#       in_out_times.in_out_times(),
    ]


def oneTime():
    for claculater in tqdm(claculaters1):
        claculater.calculate()
           
    # 关闭数据库
    for claculater in tqdm(claculaters1):
        claculater.tearDown()


def nTimes():
    from background_program.z_Tools import MyDataBase
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
        for claculater in claculaters2:
            claculater.setStudentNum(student)
            claculater.calculate()
    
    # 关闭数据库
    for claculater in tqdm(claculaters2):
        claculater.tearDown()


if __name__ == '__main__':
#     oneTime()
#     nTimes()
    for claculater in tqdm(claculaters1):
            claculater.cluster()
#   
#     for claculater in tqdm(claculaters2):
#             claculater.cluster()
    pass
