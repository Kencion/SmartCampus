'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from teacher_client.views import Search_student_info
from background_program.y_Modules.missing_warning import missing_warning


def get_missing_students():
    """
            更新数据
    @return 
    """
    """
            获得可能失联的学生的学号，
            并在数据mydatabase表student_client_Student中
            将该学生的is_missing字段设为True
    """
    missing_students = missing_warning.get_missing_students()
#     for i in missing_students:
#         Student(student_num=i, is_missing=True).save()
    return missing_students
        
# def get_missing_students():
#     """
#     @return list missing_students:可能失踪的学生
#     """
#     missing_students = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]
#     
#     return missing_students
