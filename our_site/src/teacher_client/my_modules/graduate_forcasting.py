'''
Forcasting weather a student can graduate or not

Created on 2018年4月20日

@author: Jack
'''
from student_client.models import Student
from teacher_client.models import my_module
from .processer import data_processer
from background_program.y_Modules.graduate_forcasting import graduate_forcasting

module_name = 'graduate_forcasting'
Data_processer = data_processer(module_name, my_module, graduate_forcasting)


def get_data_update():
    """
    @param
    @return
    """

    # 获取准确率，并且保存预测结果
    evaluate_score, students_and_graduates = graduate_forcasting().predict()

    for i in students_and_graduates:
        try:
            student = Student.objects.get(student_num=i[0])
        except:
            student = Student(student_num=i[0])

        student.graduate = i[1]
        student.save()

    try:
        m = my_module.objects.get(module_name=module_name)
    except:
        m = my_module(module_name=module_name)
    m.evaluate_score = evaluate_score
    m.save()

    get_feature_scores_and_ranges(data_update=True)
    get_pie_data(data_update=True)


def get_all_students_and_graduates():
    """
    获得所有学生的学号和成绩
    @return list(list()) students_and_scores,
    """
    students_and_graduates = [[i.student_num, i.graduate]
                              for i in Student.objects.order_by('-graduate')]
    return students_and_graduates


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
    @return feature_scores_and_ranges
    """

    feature_scores_and_ranges = Data_processer.get_feature_scores_and_ranges(
        data_update)

    return feature_scores_and_ranges


def get_pie_data(data_update=False):
    """
    获得成绩预测饼图数据
    @return pie_data
    """

    pie_data = Data_processer.get_pie_data(counter={'可以毕业': 0, '不可以毕业': 0},
                                           condition=[(0, 1), (1, 2)],
                                           data_update=data_update)

    return pie_data
