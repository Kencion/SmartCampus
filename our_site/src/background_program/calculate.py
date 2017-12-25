'''
Created on 2017年11月21日
  
@author: jack
细化聚类流程
'''
# import warnings
# warnings.filterwarnings("ignore")
 
from background_program.b_SampleProcessing.FeatureCalculating.activities import *
from background_program.b_SampleProcessing.FeatureCalculating.dorm_entrance import *
from background_program.b_SampleProcessing.FeatureCalculating.library import *
from background_program.b_SampleProcessing.FeatureCalculating.scholarship import *
from background_program.b_SampleProcessing.FeatureCalculating.score import *
from background_program.b_SampleProcessing.FeatureCalculating.social_practice import *
from background_program.b_SampleProcessing.FeatureCalculating.subsidy import *
from background_program.b_SampleProcessing.FeatureCalculating.hornorary_title import *
from background_program.b_SampleProcessing.FeatureCalculating.card import *
from tqdm import tqdm  

claculaters = [  
#         activity_avg_level1.activity_avg_level1(),
#         activity_last_time1.activity_last_time1(),#
#         activity_num1.activity_num1(),
#         participation_avg_point1.participation_avg_point1(),
#         avg_out_time.avg_out_time(),#
#         avg_in_time.avg_in_time(),
#         avg_stay_out_time.avg_stay_out_time(),
        in_out_times.in_out_times(),
        hornorary_rank.hornorary_rank(),
        hornorary_times.hornorary_times(),
#         library_borrow_times1.library_borrow_times1(),
        library_entrance.library_entrance(),
#         failed_num1.failed_num1(),
#         GPA1.GPA1(),
#         score_rank1.score_rank1(),
#         score1.score1(),
#         is_social_practice_great1.is_social_practice_great1(),
#         social_practice1.social_practice1(),
#         canteen_times.canteen_times(),
#         Consumption.Consumption(),
#         max_every_type.max_every_type(),
#         mean_median_var.mean_median_var(),
#         total_amount_every_type.total_amount_every_type(),
#         transaction_times.transaction_times(),
#         canteen_consumption_divide_by_consumption.canteen_consumption_divide_by_consumption(),
#         library_study_time.library_study_time(),
        library_week_study_time.library_week_study_time(),
        scholarship_amount.scholarship_amount(),
        scholarship_rank.scholarship_rank(),
        subsidy_amount.subsidy_amount(),
        subsidy_rank.subsidy_rank(),
    ]



def calculate():
    for claculater in tqdm(claculaters):
        claculater.calculate()
        claculater.tearDown()
           
def clean_useless_data():
    from background_program.z_Tools.my_database import MyDataBase
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = ""
    executer.execute(sql)
    db.tearDown()


def doit():
#     # 先插入学号
#     from background_program.b_SampleProcessing.FeatureCalculating.FeatureCalculater import FeatureCalculater
#     FeatureCalculater().calculate()
    
    # 计算特征值
    calculate()
    
#     # 把没用的数据清除掉
#     clean_useless_data()
#     
#     # 聚类
#     for claculater in tqdm(claculaters):
#             claculater.cluster()
    pass


if __name__ == '__main__':
    doit()
    
