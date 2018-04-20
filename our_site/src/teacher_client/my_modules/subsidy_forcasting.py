'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from teacher_client.models import my_module
from background_program.y_Modules.subsidy_forcasting import subsidy_forcasting
from .processer import data_processer

module_name = 'subsidy_forcasting'
Data_processer = data_processer(module_name, my_module, subsidy_forcasting)


def get_data_update():
    """
            更新数据
    @return 
            获得所有学生的成绩预测记过，
            并在数据mydatabase表student_client_Student中
            将该学生的subsidy字段设为预测结果
    """
    evaluate_score, students_and_subsidies = subsidy_forcasting().predict()
    for i in students_and_subsidies:
        try:
            student = Student.objects.get(student_num=i[0])
        except:
            student = Student(student_num=i[0])
        student.subsidy = i[1]
        student.save()

    get_evaluate_score(evaluate_score, data_update=True)
    get_feature_scores_and_ranges(data_update=True)
    get_pie_data(data_update=True)


def get_students_and_subsidies():
    """
            获得所有学生的学号和成绩
    @return list(list()) students_and_scores,
    """
    students_and_subsidies = [[i.student_num, i.subsidy]
                              for i in Student.objects.order_by('-subsidy')]

    return students_and_subsidies


def get_evaluate_score():
    '''
    获取成绩预测模块可信度分数
    '''
    try:
        return my_module.objects.get(module_name=module_name).evaluate_score
    except:
        pass

    return 0


def get_feature_scores_and_ranges(data_update=False):
    """
    获得90分以上、60分以下的学生的特征范围
    @return list() class_failed_students,
    """
    feature_scores_and_ranges = Data_processer.get_feature_scores_and_ranges('tree', data_update)

    return feature_scores_and_ranges


def get_pie_data(data_update=False):
    """
            获得成绩预测饼图数据
    @return pie_data
    """

    pie_data = Data_processer.get_pie_data(counter={'未获得助学金': 0, '获得助学金': 0},
                                           condition=[
                                               (-9999999, 0.0000001), (0.0000001, 9999999)],
                                           data_update=data_update)

    return pie_data
