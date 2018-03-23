'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from teacher_client.models import my_module
from background_program.y_Modules.subsidy_forcasting import subsidy_forcasting


def get_data_update():
    """
            更新数据
    @return 
    """
    """
            获得所有学生的成绩预测记过，
            并在数据mydatabase表student_client_Student中
            将该学生的subsidy字段设为预测结果
    """
    evaluate_score, students_and_subsidies = subsidy_forcasting().predict()
    for i in students_and_subsidies:
        Student(student_num=i[0], subsidy=i[1]).save()
        
        
    my_module.objects.filter(module_name='scholarship_forcasting').delete()
    my_module(module_name='subsidy_forcasting', evaluate_score=evaluate_score, feature_scores_and_ranges='', pie_data='').save()
    get_feature_scores_and_ranges(update=True)
    get_pie_data(update=True)


def get_students_and_subsidies():
    """
            获得所有学生的学号和成绩
    @return list(list()) students_and_scores,
    """
    students_and_subsidies = [[i.student_num, i.subsidy] for i in Student.objects.order_by('subsidy')]
    
    return students_and_subsidies


def  get_evaluate_score():
    evaluate_score = 0
    try:
        evaluate_score = my_module.objects.filter(module_name='scholarship_forcasting')[0].evaluate_score
    except:
        pass
     
    return evaluate_score


def get_feature_scores_and_ranges(update=False):
    """
            获得90分以上、60分以下的学生的特征范围
    @return list() class_failed_students,
    """
    try:
        feature_scores_and_ranges = eval(my_module.objects.filter(module_name='subsidy_forcasting')[0].feature_scores_and_ranges)
        if update:
            feature_scores_and_ranges = subsidy_forcasting().get_tree_data()
            my_module.objects.filter(module_name='subsidy_forcasting').update(feature_scores_and_ranges=feature_scores_and_ranges)
    except:
        feature_scores_and_ranges = subsidy_forcasting().get_tree_data()
        my_module.objects.filter(module_name='subsidy_forcasting').update(feature_scores_and_ranges=feature_scores_and_ranges)
        
    return feature_scores_and_ranges


def get_pie_data(update=False):
    """
            获得90分以上、60分以下的学生的特征范围
    @return list() class_failed_students,
    """
    try:
        pie_data = eval(my_module.objects.filter(module_name='subsidy_forcasting')[0].pie_data)
        if update:
            pie_data = subsidy_forcasting().get_pie_data()
            my_module.objects.filter(module_name='subsidy_forcasting').update(pie_data=pie_data)
    except:
        pie_data = subsidy_forcasting().get_pie_data()
        my_module.objects.filter(module_name='subsidy_forcasting').update(pie_data=pie_data)
        
    return pie_data
