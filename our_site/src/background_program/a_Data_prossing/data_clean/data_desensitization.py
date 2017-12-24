'''
Created on 2017年12月20日
数据脱敏到“软件学院脱敏”数据库中
@author: Jack
'''


def doit():
    """
            将students表中的中文字符串改为数字，方便后续处理
    @params
    @return
    """
    from background_program.z_Tools import MyDataBase
    
    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "INSERT \
            INTO 软件学院脱敏.students\
            SELECT `student_num`, `student_type`, `activity_num`, `activity_avg_level`, `activity_last_time`, `participation_avg_point`, `hornorary_rank`, `hornorary_times`, `library_borrow_times`, `library_study_time`, `library_week_study_time`, `gpa`, `score_rank`, `subsidy_rank`, `subsidy_amount`, `failed_num`, `failed_pass_num`, `failed_failed_num`, `social_practice_time`, `is_social_practice_great`, `in_out_times`, `student_grade`, `scholarship_rank`, `scholarship_amount`, `score`, `avg_out_time`, `avg_in_time`, `avg_stay_out_time`, `canteen_total_amount`, `market_total_amount`, `other_total_amount`, `charge_total_amount`, `snack_total_amount`, `exercise_total_amount`, `study_total_amount`, `charge_day_max_amount`, `exercise_day_max_amount`, `snack_day_max_amount`, `study_day_max_amount`, `market_day_max_amount`, `canteen_day_max_amount`, `other_day_max_amount`, `charge_max_amount`, `exercise_max_amount`, `snack_max_amount`, `study_max_amount`, `canteen_max_amount`, `market_max_amount`, `other_max_amount`, `charge_min_amount`, `exercise_min_amount`, `snack_min_amount`, `study_min_amount`, `canteen_min_amount`, `market_min_amount`, `other_min_amount`, `transaction_times`, `canteen_amount_divide_by_consumption`, `canteen_times`, `Consumption`, `median_of_canteen`, `median_of_market`, `median_of_charge`, `median_of_snack`, `median_of_exercise`, `median_of_study`, `median_of_other`, `mean_of_canteen`, `mean_of_market`, `mean_of_charge`, `mean_of_snack`, `mean_of_exercise`, `mean_of_study`, `mean_of_other`, `var_of_canteen`, `var_of_market`, `var_of_charge`, `var_of_other`, `var_of_snack`, `var_of_exercise`, `var_of_study` \
            FROM 软件学院.students \
            WHERE \
                score is not null\
                AND gpa is not null"
    
    executer.execute(sql)
    db.close()

    db = MyDataBase.MyDataBase("软件学院")
    executer = db.getExcuter()

    sql = "select * from students where 1=1"
    
    executer.execute(sql)
    db.close()

if __name__ == '__main__':
    doit()