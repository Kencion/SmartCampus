'''
Modify on 2018年1月15日

@author: Jack
'''
from django.shortcuts import loader
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from student_client.models import Student
from our_site.my_logger import exception_handler
from our_site.my_exceptions import not_login_exception
from .my_modules.processer import data_page_processer
from audioop import reverse

Data_page_processer = data_page_processer()


@exception_handler
def index(request, update=False):
    """
    @return 智慧校园_教师端_主页
    """
    from .my_modules import missing_warning, score_forcasting, scholarship_forcasting, subsidy_forcasting
    context = dict()
    try:
        context['teacher_name'] = request.GET['user_name']
        request.session['teacher_name'] = context['teacher_name']
        context['update'] = request.GET['update']
    except:
        pass 
    try:
        context['teacher_name'] = request.session['teacher_name']
    except:
        raise not_login_exception 
    
    context['student_nums'] = missing_warning.get_missing_students()
    context['score_pie_chart'] = Data_page_processer.get_pie_page('score_pie_chart', score_forcasting.get_pie_data(), request)
    context['scholarship_pie_chart'] = Data_page_processer.get_pie_page('scholarship_pie_chart', scholarship_forcasting.get_pie_data(), request)
    context['subsidy_pie_chart'] = Data_page_processer.get_pie_page('subsidy_pie_chart', subsidy_forcasting.get_pie_data(), request)

    template = loader.get_template('teacher_client/index.html')
    return HttpResponse(template.render(context, request))


@exception_handler
def missing_warning(request, update=False):
    """
    @return: 失联预警_页面
    """
    from .my_modules import missing_warning 
    try:
        update = request.GET['update']
        if update:  # 如果需要更新数据
            missing_warning.get_data_update()
             
        return HttpResponseRedirect('/teacher_client/missing_warning')
    except:
        pass
    
    missing_students = missing_warning.get_missing_students()
    
    context = {
        'module_name':'失联预警',
        'teacher_name':request.session['teacher_name'],
        'missing_students':missing_students,
        }
    template = loader.get_template('teacher_client/missing_warning.html')
    
    return HttpResponse(template.render(context, request))

    
@exception_handler
def score_forcasting(request):
    """
    @return: 成绩预测_页面
    """
    from .my_modules import score_forcasting
    try:
        if request.GET['update']:  # 如果需要更新数据
            score_forcasting.get_data_update()
        return HttpResponseRedirect('/teacher_client/score_forcasting')
    except:
        pass
    
    context = {
       'teacher_name':request.session['teacher_name'],
       'evaluate_score':score_forcasting.get_evaluate_score(),
       'students_and_scores':score_forcasting.get_all_students_and_scores(),
       'class_fail_student_nums':score_forcasting.get_class_failed_students(),
       'feature_scores_and_ranges':Data_page_processer.get_feature_ranges_tree_page(score_forcasting.get_feature_scores_and_ranges(), request),
       'score_pie_chart':Data_page_processer.get_pie_page('score_pie_chart', score_forcasting.get_pie_data(), request),
       }
        
    score_forcasting_page = loader.get_template('teacher_client/score_forcasting.html')
    
    return HttpResponse(score_forcasting_page.render(context, request))


@exception_handler
def scholarship_forcasting(request):
    """
    @return: 奖学金预测_页面
    """
    from .my_modules import scholarship_forcasting 
    try:
        if request.GET['update']:  # 如果需要更新数据
            scholarship_forcasting.get_data_update()
            
        return HttpResponseRedirect('/teacher_client/scholarship_forcasting')
    except:
        pass
    
    students_and_scholarships = scholarship_forcasting.get_students_and_scholarships()

    context = {
        'module_name':'成绩预测',
        'teacher_name':request.session['teacher_name'],
        'evaluate_score':scholarship_forcasting.get_evaluate_score(),
        'students_and_scores':students_and_scholarships,
        'feature_scores_and_ranges':Data_page_processer.get_feature_ranges_tree_page(scholarship_forcasting.get_feature_scores_and_ranges(), request),
        'scholarship_pie_chart':Data_page_processer.get_pie_page('scholarship_pie_chart', scholarship_forcasting.get_pie_data(), request),
        }
    template = loader.get_template('teacher_client/scholarship_forcasting.html')
    
    return HttpResponse(template.render(context, request))


@exception_handler
def subsidy_forcasting(request):
    """
    @return: 奖学金预测_页面
    """
    from .my_modules import subsidy_forcasting 
    try:
        if request.GET['update']:  # 如果需要更新数据
            subsidy_forcasting.get_data_update()
            
        return HttpResponseRedirect('/teacher_client/subsidy_forcasting')
    except:
        pass
    
    students_and_subsidies = subsidy_forcasting.get_students_and_subsidies()

    context = {
        'module_name':'助学金预测',
        'teacher_name':request.session['teacher_name'],
        'evaluate_score':subsidy_forcasting.get_evaluate_score(),
        'students_and_subsidies':students_and_subsidies,
        'feature_scores_and_ranges':Data_page_processer.get_feature_ranges_tree_page(subsidy_forcasting.get_feature_scores_and_ranges(), request),
        'subsidy_pie_chart':Data_page_processer.get_pie_page('subsidy_pie_chart', subsidy_forcasting.get_pie_data(), request),
        }
    template = loader.get_template('teacher_client/subsidy_forcasting.html')
    
    return HttpResponse(template.render(context, request))


@exception_handler
def graduate_forcasting(request):
    """
    @author: jack
    @return: 毕业预测_页面
    """
    from .my_modules import graduate_forcasting
    try:
        if request.GET['update']:  # 如果需要更新数据
            graduate_forcasting.get_data_update()
        return HttpResponseRedirect('/teacher_client/graduate_forcasting')
    except:
        pass
    
    types, top_10_features, top_10_feature_range = graduate_forcasting.get_feature_scores_and_ranges()
    
    context = {
       'teacher_name':request.session['teacher_name'],
       'evaluate_score':graduate_forcasting.get_evaluate_score(),
       'students_and_graduates':graduate_forcasting.get_all_students_and_graduates(),
       'graduate_fail_students':graduate_forcasting.get_graduate_fail_students(),
       
       'feature_scores_and_ranges':Data_page_processer.get_feature_ranges_radar_page(
           types, top_10_features, top_10_feature_range,
           request),
       
       'graduate_pie_chart':Data_page_processer.get_pie_page(
           'graduate_pie_chart',
           graduate_forcasting.get_pie_data(),
           request),
       }
        
    graduate_forcasting_page = loader.get_template('teacher_client/graduate_forcasting.html')
    
    return HttpResponse(graduate_forcasting_page.render(context, request))


@exception_handler
def wired_person(request, update=False):
    """
    @return: 奇怪的人_页面
    """
    try:
        update = request.GET['update']
        if update:  # 如果需要更新数据
            from background_program.y_Modules import missing_warning
            missing_students = missing_warning.get_missing_students()
            for i in missing_students:
                Student(student_num=i, is_missing=True).save()
            
            return HttpResponseRedirect('/teacher_client/score_forcasting')
    except:
        pass
    
    missing_students = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]
    context = {
        'module_name':'失联预警',
        'teacher_name':request.session['teacher_name'],
        'student_nums':missing_students,
        }
    template = loader.get_template('teacher_client/wired_person.html')
    
    return HttpResponse(template.render(context, request))


def student_info(request):
    """
    @return: 学生信息_页面
    """
    from student_client.dataprocess.student_data import get_students_info
    from student_client.views import get_single_student_info
    
    student_num = request.GET['student_num']
    
    context = {
        'module_name':'学生信息',
        'student_info_page':get_students_info(get_single_student_info(student_num), request),
        }
    template = loader.get_template('teacher_client/student_info.html')
    
    return HttpResponse(template.render(context, request))
    

def not_login(request):
    """
    @return: 错误处理_未登录_页面
    """
    template = loader.get_template('teacher_client/error_pages/not_login.html')
    
    return HttpResponse(template.render(None, request))
