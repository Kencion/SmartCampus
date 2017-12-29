from django.shortcuts import render, loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from student_client.models import Student
# Create your views here.

def index(request):
    """
    @author: yhj
    @modify: jack
    @return: 填一下
    """
    try:
        student_num = request.GET['user_name']
        request.session['student_num'] = student_num
    except:
        pass
    
    try:
        student_num = request.session['student_num']  
    except:
        pass
    
    response = Student.objects.filter(student_num__startswith=student_num)
    result = []
    for re in response:
        if int(re.score) == 2:
            result.append("注意，你有可能挂科咯")
    request.session['result'] = result
    
    context = {
        "UserName":student_num,
        "result":result,
        }
    template = loader.get_template('student_client/index.html')
    return HttpResponse(template.render(context, request))
def show_student_info(request):
    from background_program.z_Tools.my_database import MyDataBase
    student_num=request.session.get('student_num')
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "select student_name,student_type,activity_num,activity_avg_level,activity_last_time,library_borrow_times,library_study_time,student_grade,scholarship_amount,scholarship_rank,failed_num,failed_pass_num,failed_failed_num,score,score_rank,gpa from students where student_num like '{0}%'".format(student_num)
    executer.execute(sql)
    students_list = executer.fetchall()
    student_name=students_list[0][0]
    db.close 
    template = loader.get_template('student_client/show_student_info.html')
    context = {
        'student_num':student_num,
        'student_name':student_name,
        'result':students_list,
    }
    return HttpResponse(template.render(context, request))
def Single_student(request):
    """
    @author: 
    @modify: jack
    @return: 填一下
    """
    
    template = loader.get_template('student_client/input.html')
    context = {
        'student_num':request.session['student_num'] ,
    }
    return HttpResponse(template.render(context, request))

def search_score(request):
    """
    @author: 
    @return: 填一下
    """
    from background_program.z_Tools.my_database import MyDataBase
    
    try:
        student_num = request.session['student_num']  
    except:
        pass
    
    student_num = request.POST['student_num']
    year = request.POST['year']
    student_num = student_num + year
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "select student_num,student_name,student_grade,score_rank,score from students where student_num='{0}'".format(student_num)
    executer.execute(sql)
    student = executer.fetchone()
    db.close 
    # print(student)
    if student is None:
        template = loader.get_template('student_client/input.html')
        context = {
            'title':"hello, my dear student, please input your student_num and school_year: ",
            'result':"Sorry,I can't find the student_num or shool_year.",
            }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('student_client/search_score.html')
        context = {
            'student_num':student[0],
            'student_name':student[1],
            'student_grade':student[2],
            'score_rank':student[3],
            'score':student[4],
        }
        return HttpResponse(template.render(context, request))
