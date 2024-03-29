'''
@author: jack on 2017年11月21日
'''
# import warnings
# warnings.filterwarnings("ignore")
 
from background_program.b_Sample_processing.Feature_calculating.activitie import activity_avg_level1, activity_last_time1, activity_num1, participation_avg_point1
from background_program.b_Sample_processing.Feature_calculating.dorm_entrance import in_out_times, avg_in_time, avg_out_time, avg_stay_out_time
from background_program.b_Sample_processing.Feature_calculating.library import library_study_time, library_week_study_time, library_borrow_times1, library_entrance
from background_program.b_Sample_processing.Feature_calculating.scholarship import scholarship_amount, scholarship_rank
from background_program.b_Sample_processing.Feature_calculating.score import department, failed_num1, GPA1, school_year1, score_rank1, score1, failed_failed_num, failed_pass_num
from background_program.b_Sample_processing.Feature_calculating.social_practice import is_social_practice_great1, social_practice_time
from background_program.b_Sample_processing.Feature_calculating.subsidy import subsidy_rank, subsidy_amount
from background_program.b_Sample_processing.Feature_calculating.hornorary_title import hornorary_rank, hornorary_times
from background_program.b_Sample_processing.Feature_calculating.card import canteen_consumption_divide_by_consumption, canteen_times, Consumption, max_every_type, max_min_month_consume, mean_median_var, total_amount_every_type, transaction_times
from tqdm import tqdm  

calculaters = [  
#         activity_avg_level1.activity_avg_level1(),
#         activity_last_time1.activity_last_time1(),
#         activity_num1.activity_num1(),
#         participation_avg_point1.participation_avg_point1(),
#             
#         avg_out_time.avg_out_time(),
#         avg_in_time.avg_in_time(),
#         avg_stay_out_time.avg_stay_out_time(),
#         in_out_times.in_out_times(),
#             
#         library_borrow_times1.library_borrow_times1(),
#         library_entrance.library_entrance(),
#         library_study_time.library_study_time(),
#         library_week_study_time.library_week_study_time(),
#             
#         scholarship_amount.scholarship_amount(),
#         scholarship_rank.scholarship_rank(),
#             
#         department.department(),
#         school_year1.school_year1(),
#         failed_num1.failed_num1(),
#         failed_pass_num.failed_pass_num(),
#         failed_failed_num.failed_failed_num(),
#         GPA1.GPA1(),
#         score_rank1.score_rank1(),
        score1.score1(),
#             
#         is_social_practice_great1.is_social_practice_great1(),
#         social_practice_time.social_practice_time(),
#         subsidy_amount.subsidy_amount(),
#         subsidy_rank.subsidy_rank(),
#            
#         hornorary_rank.hornorary_rank(),
#         hornorary_times.hornorary_times(),
#            
#         canteen_times.canteen_times(),
#         Consumption.Consumption(),
#         max_min_month_consume.max_min_month_consume(),
#         max_every_type.max_every_type(),
#         mean_median_var.mean_median_var(),
#         total_amount_every_type.total_amount_every_type(),
#         transaction_times.transaction_times(),
#         canteen_consumption_divide_by_consumption.canteen_consumption_divide_by_consumption(),
        
    ]


def calculate():
    for claculater in tqdm(calculaters):
        claculater.calculate()
        claculater.tearDown()

           
def clean_useless_data():
    from background_program.z_Tools.my_database import MyDataBase
#     try:
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "SELECT *\
            FROM\
                students\
            WHERE\
                score IS NOT NULL\
            AND canteen_times IS NOT NULL"
    executer.execute(sql)
    results = [list(i) for i in executer.fetchall()]
    for i in range(len(results)):
        for j in range(len(results[i])):
            if results[i][j] is None:
                results[i][j] = 0
        sql = "insert into students_float values{0}".format(tuple(results[i]))
        executer.execute(sql)
    
    db.close()
#     except:
#         pass


def doit():
#     # 先插入学号
#     from background_program.b_Sample_processing.Feature_calculating.FeatureCalculater import FeatureCalculater
#     FeatureCalculater().calculate()
#     
#     # 计算特征值
#     calculate()
#      
#     # 把没用的数据清除掉
#     clean_useless_data()
    
#     # 聚类
    for calculater in tqdm(calculaters):
            calculater.cluster()
            calculater.tearDown()


if __name__ == '__main__':
    doit()
