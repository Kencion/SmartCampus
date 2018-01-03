'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
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
    from .draw_pics import pie_chart, line_chart, broken_line_chart
    pie_chart(), line_chart(), broken_line_chart()
    _, students_and_subsidies = subsidy_forcasting().doit()
    for i in students_and_subsidies:
        Student(student_num=i[0], subsidy=i[1]).save()


def get_students_and_subsidies():
    """
            获得所有学生的学号和成绩
    @return list(list()) students_and_scores,
    """
    students_and_subsidies = [[i.student_num, i.subsidy] for i in Student.objects.order_by('subsidy')]
    
    return students_and_subsidies

