'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from student_client.views import Search_student_info
from background_program.y_Modules import missing_warning


def get_data_update():
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
    student_nums = list(missing_students.keys())
    for student_num in student_nums:
        try:
            student_name = Search_student_info(student_num)['姓名']
            Student(student_num=student_num,
                    student_name=student_name,
                    is_missing=True,
                    missing_reason=missing_students[student_num]
                    ).save()
        except:
            pass

        
def get_missing_students():
    """
    @return list missing_students:可能失踪的学生
    """
    missing_students = [[i.student_num, i.student_name, i.missing_reason] for i in Student.objects.filter(is_missing__exact=True)]
     
    return missing_students


if __name__ == '__main__':
    get_missing_students()
