from django.shortcuts import loader
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from student_client.models import Student
from our_site.my_logger import exception_handler
from our_site.my_exceptions import not_login_exception


@exception_handler
def index(request, update=False):
    """
    @author: Jack
    @return 教师端的主页
    """
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
    
    context['student_nums'] = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]

    template = loader.get_template('teacher_client/index.html')
    return HttpResponse(template.render(context, request))

    
@exception_handler
def score_forcasting(request, update=False):
    """
    @author: Jack
    @return: 成绩预测页面
    """
    from .my_modules import score_forcasting
    try:
        update = request.GET['update']
        if update:  # 如果需要更新数据
            score_forcasting.get_data_update()
        return HttpResponseRedirect('/teacher_client/score_forcasting')
    except:
        pass
    
    """获取挂科的同学的学号"""    
    students_and_scores = score_forcasting.get_all_students_and_scores()
    class_failed_students = score_forcasting.get_class_failed_students()

    context = {
        'module_name':'成绩预测',
        'teacher_name':request.session['teacher_name'],
        'students_and_scores':students_and_scores,
        'class_fail_student_nums':class_failed_students,
        }
    template = loader.get_template('teacher_client/score_forcasting.html')
    
    return HttpResponse(template.render(context, request))


@exception_handler
def missing_warning(request, update=False):
    """
    @author: Jack
    @return: 失联预警页面
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
def scholarship_forcasting(request, update=False):
    """
            奖学金预测页面
    @author: Jack
    @return: 奖学金预测页面
    """
    from .my_modules import scholarship_forcasting 
    try:
        update = request.GET['update']
        if update:  # 如果需要更新数据
            scholarship_forcasting.get_data_update()
            
        return HttpResponseRedirect('/teacher_client/scholarship_forcasting')
    except:
        pass
    
    students_and_scholarships = scholarship_forcasting.get_students_and_scholarships()

    context = {
        'module_name':'成绩预测',
        'teacher_name':request.session['teacher_name'],
        'students_and_scores':students_and_scholarships,
        }
    template = loader.get_template('teacher_client/scholarship_forcasting.html')
    
    return HttpResponse(template.render(context, request))


@exception_handler
def subsidy_forcasting(request):
    """
            助学金预测页面
    @author: Jack
    @return: 奖学金预测页面
    """
    from .my_modules import subsidy_forcasting 
    try:
        update = request.GET['update']
        if update:  # 如果需要更新数据
            subsidy_forcasting.get_data_update()
            
        return HttpResponseRedirect('/teacher_client/subsidy_forcasting')
    except:
        pass
    
    students_and_subsidies = subsidy_forcasting.get_students_and_subsidies()

    context = {
        'module_name':'助学金预测',
        'teacher_name':request.session['teacher_name'],
        'students_and_subsidies':students_and_subsidies,
        }
    template = loader.get_template('teacher_client/subsidy_forcasting.html')
    
    return HttpResponse(template.render(context, request))


@exception_handler
def wired_person(request, update=False):
    """
            奇怪的人页面
    @author: Jack
    @return: 奇怪的人页面
    """
    try:
        update = request.GET['update']
        if update:  # 如果需要更新数据
            from background_program.y_Modules.missing_warning import missing_warning
            missing_students = missing_warning.get_missing_students()
            for i in missing_students:
                Student(student_num=i, is_missing=True).save()
            
            return HttpResponseRedirect('/teacher_client/score_forcasting')
    except:
        pass
    
    missing_students = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]
    """将数据渲染到页面上"""
    context = {
        'module_name':'失联预警',
        'teacher_name':request.session['teacher_name'],
        'student_nums':missing_students,
        }
    template = loader.get_template('teacher_client/wired_person.html')
    
    return HttpResponse(template.render(context, request))


def not_login(request):
    template = loader.get_template('teacher_client/error_pages/not_login.html')
    
    return HttpResponse(template.render(None, request))