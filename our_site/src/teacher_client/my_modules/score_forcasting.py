'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting


def get_lastest_data():
    """
            获得所有学生的成绩预测结果，
            并在数据mydatabase表student_client_Student中
            将该学生的score字段设为预测结果
    """
#     pie_chart(), line_chart(), broken_line_chart()
    _, students_and_scores = score_forcasting().doit()
    for i in students_and_scores:
        Student(student_num=i[0], score=i[1]).save()


def get_students():
    students_and_scores = [[i.student_num, i.score] for i in Student.objects.all()]
    """获取挂科的同学的学号"""    
    class_fail_student_nums = [i.student_num for i in Student.objects.filter(score__lt=60.0)]
    
    return students_and_scores, class_fail_student_nums

def get_all_students_and_scores():
    students_and_scores = [[i.student_num, i.score] for i in Student.objects.all()]
    return students_and_scores

def get_
    
def get_feature_range():
    _,class_fail_student_nums=get_students
