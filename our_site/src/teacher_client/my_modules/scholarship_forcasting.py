'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from background_program.y_Modules.scholarship_forcasting.scholarship_forcasting import scholarship_forcasting


def get_data_update():
    """
            更新数据
    @return 
    """
    """
            获得所有学生的成绩预测记过，
            并在数据mydatabase表student_client_Student中
            将该学生的score字段设为预测结果
    """
#     pie_chart(), line_chart(), broken_line_chart()
    _, students_and_scholarships = scholarship_forcasting().doit()
    for i in students_and_scholarships:
        Student(student_num=i[0], scholarship=i[1]).save()


def get_students_and_scholarships():
    """
            获得所有学生的学号和成绩
    @return list(list()) all_students
    """
    students_and_scholarships = [[i.student_num, i.scholarship] for i in Student.objects.all()]
    
    return students_and_scholarships
    
