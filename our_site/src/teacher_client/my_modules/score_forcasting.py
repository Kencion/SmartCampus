'''
Created on 2017年12月29日

@author: Jack
'''
from student_client.models import Student
from teacher_client.models import my_module
from .processer import data_processer
from background_program.y_Modules.score_forcasting import score_forcasting

module_name = 'score_forcasting'
Data_processer = data_processer(module_name, my_module, score_forcasting)


def get_data_update():
    """
    @param  
    @return 
    """
    
    # 获取准确率，并且保存预测结果
    evaluate_score, students_and_scores = score_forcasting().predict()
    for i in students_and_scores:
        Student(student_num=i[0], score=i[1]).save()
    
    my_module.objects.filter(module_name).delete()
    my_module(
        module_name=module_name,
        evaluate_score=evaluate_score,
        feature_scores_and_ranges='',
        pie_data='').save()
    get_feature_scores_and_ranges(data_update=True)
    get_pie_data(data_update=True)


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


def get_evaluate_score(data_update=False):
    '''
            获取成绩预测模块可信度分数
    '''
    evaluate_score = Data_processer.get_evaluate_score(data_update)
    
    return evaluate_score

    
def get_feature_scores_and_ranges(data_update=False):
    """
            获得90分以上、60分以下的学生的特征范围
    @return feature_scores_and_ranges
    """
    
    feature_scores_and_ranges = Data_processer.get_feature_scores_and_ranges(data_update)
    
    return feature_scores_and_ranges


def get_pie_data(data_update=False):
    """
            获得成绩预测饼图数据
    @return pie_data
    """
    
    pie_data = Data_processer.get_pie_data(counter={'60分以下': 0, '60分-70分': 0, '70分-80分': 0, '80分-90分': 0, '90分及以上': 0},
                                           condition=[(0, 60), (60, 70), (70, 80), (80, 90), (90, 101)],
                                           data_update=data_update)
    
    return pie_data
