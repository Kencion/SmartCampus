from django.shortcuts import loader
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from student_client.models import Student
from our_site.my_logger import exception_handler
from our_site.my_exceptions import not_login_exception
# Create your views here.


@exception_handler
def index(request, update=False):
    """
            教师端的主页
    @author: Jack
    @return 教师端的主页
    """
    context = dict()
    try:
        context['teacher_name'] = request.GET['user_name']
        request.session['teacher_name'] = context['teacher_name']
#         context['update'] = request.GET['update']
    except:
        pass 
    try:
        context['teacher_name'] = request.session['teacher_name']
    except:
        raise not_login_exception 
    
    """从数据库获得失联学生的学号"""
    context['student_nums'] = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]

    """将数据渲染到页面上"""
    template = loader.get_template('teacher_client/index.html')
    return HttpResponse(template.render(context, request))

    
@exception_handler
def score_forcasting(request, update=False):
    """
            成绩预测页面
    @author: Jack
    @return: 成绩预测页面
    """
    try:
        """如果需要更新数据"""
        update = request.GET['update']
        if update:
            from .my_modules.score_forcasting import get_lastest_data 
            get_lastest_data()
        return HttpResponseRedirect('/teacher_client/score_forcasting')
    except:
        pass
    
    """获取挂科的同学的学号"""    
    from .my_modules.score_forcasting import get_students
    students_and_scores, class_fail_student_nums = get_students()

    """将数据渲染到页面上"""
    context = {
        'module_name':'成绩预测',
        'teacher_name':request.session['teacher_name'],
        'students_and_scores':students_and_scores,
        'class_fail_student_nums':class_fail_student_nums,
        }
    template = loader.get_template('teacher_client/score_forcasting.html')
    
    return HttpResponse(template.render(context, request))


@exception_handler
def missing_warning(request, update=False):
    """
            失联预警页面
    @author: Jack
    @return: 失联预警页面
    """
    """
            获得可能失联的学生的学号，
            并在数据mydatabase表student_client_Student中
            将该学生的is_missing字段设为True
    """
    try:
        """如果需要更新数据"""
        update = request.GET['update']
        if update:
            from background_program.y_Modules.missing_warning import missing_warning
            missing_students = missing_warning.doit()
            for i in missing_students:
                Student(student_num=i, is_missing=True).save()
            
            return HttpResponseRedirect('/teacher_client/missing_warning')
    except:
        pass
    
    missing_students = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]
    """将数据渲染到页面上"""
    context = {
        'module_name':'失联预警',
        'teacher_name':request.session['teacher_name'],
        'student_nums':missing_students,
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
    """
            获得所有学生的成绩预测记过，
            并在数据mydatabase表student_client_Student中
            将该学生的score字段设为预测结果
    """
    try:
        """如果需要更新数据"""
        update = request.GET['update']
        if update:
            from background_program.y_Modules.scholarship_forcasting.scholarship_forcasting import scholarship_forcasting

#             pie_chart(), line_chart(), broken_line_chart()
            _, students_and_scholarships = scholarship_forcasting().doit()
            for i in students_and_scholarships:
                Student(student_num=i[0], scholarship=i[1]).save()
        return HttpResponseRedirect('/teacher_client/scholarship_forcasting')
    except:
        pass
    
    students_and_scholarships = [[i.student_num, i.scholarship] for i in Student.objects.all()]

    """将数据渲染到页面上"""
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
    """
            获得所有学生的成绩预测记过，
            并在数据mydatabase表student_client_Student中
            将该学生的subsidy字段设为预测结果
    """
    try:
        """如果需要更新数据"""
        update = request.GET['update']
        if update:
            from background_program.y_Modules.subsidy_forcasting.subsidy_forcasting import subsidy_forcasting

#             pie_chart(), line_chart(), broken_line_chart()
            _, students_and_subsidies = subsidy_forcasting().doit()
            for i in students_and_subsidies:
                Student(student_num=i[0], subsidy=i[1]).save()
        return HttpResponseRedirect('/teacher_client/subsidy_forcasting')
    except:
        pass
    
    students_and_subsidies = [[i.student_num, i.subsidy] for i in Student.objects.order_by('subsidy')]

    """将数据渲染到页面上"""
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
        """如果需要更新数据"""
        update = request.GET['update']
        if update:
            from background_program.y_Modules.missing_warning import missing_warning
            missing_students = missing_warning.doit()
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
