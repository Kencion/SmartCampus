'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from teacher_client.models import my_module
import json


def get_precision():
    return 1


def get_data_update():
    """
            更新数据
    @return 
    """
    from background_program.y_Modules.score_forcasting import score_forcasting
    
    # 获取准确率，并且保存预测结果
    precision, students_and_scores = score_forcasting().predict()
    
    for i in students_and_scores:
        Student(student_num=i[0], score=i[1]).save()
    
#     my_module(module_name='score_forcasting', feature_scores_and_ranges='', pie_data='').save()
#     get_feature_scores_and_ranges(update=True)
#     get_pie_data(update=True)


def get_all_students_and_scores():
    """
            获得所有学生的学号和成绩
    @return list(list()) students_and_scores,
    """
    students_and_scores = [[i.student_num, i.score] for i in Student.objects.all()]
    return students_and_scores


def get_class_failed_students():
    """
            获得所有挂科学生的学号
    @return list() class_failed_students,
    """
    class_failed_students = [i.student_num for i in Student.objects.filter(score__lt=60.0)]
    return class_failed_students

    
def get_feature_scores_and_ranges(update=False):
    """
            获得90分以上、60分以下的学生的特征范围
    @return list() class_failed_students,
    """
    from background_program.y_Modules.score_forcasting import score_forcasting
    
    if update:
        feature_scores_and_ranges = score_forcasting().get_tree_data()
#         my_module.objects.filter(module_name='score_forcasting').update(feature_scores_and_ranges=feature_scores_and_ranges)
    
    else:
#         return my_module.objects.filter(module_name='score_forcasting')[0].feature_scores_and_ranges
        return score_forcasting().get_tree_data()


def get_pie_data(update=False):
    """
            获得90分以上、60分以下的学生的特征范围
    @return list() class_failed_students,
    """
    from background_program.y_Modules.score_forcasting import score_forcasting
    
    if update:
        pie_data = score_forcasting().get_pie_data()
#         my_module.objects.filter(module_name='score_forcasting').update(pie_data=pie_data)
    
    else:
#         return my_module.objects.filter(module_name='score_forcasting')[0].pie_data
        return score_forcasting().get_pie_data()
