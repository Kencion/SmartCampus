'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting


def get_lastest_data():
    """
            更新数据
    @return 
    """
#     pie_chart(), line_chart(), broken_line_chart()
    _, students_and_scores = score_forcasting().doit()
    for i in students_and_scores:
        Student(student_num=i[0], score=i[1]).save()


def get_all_students_and_scores():
    """
            获得所有学生的学号和成绩
    @return list(list()) students_and_scores,
    """
    students_and_scores = [[i.student_num, i.score] for i in Student.objects.all()]
    return students_and_scores


def get_class_failed_students():
    class_failed_students = [i.student_num for i in Student.objects.filter(score__lt=60.0)]
    return class_failed_students

    
def get_feature_range():
    class_fail_student_nums = get_class_failed_students()
