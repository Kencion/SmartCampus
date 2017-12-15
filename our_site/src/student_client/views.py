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
        student_name = request.GET['user_name']
        request.session['student_name'] = student_name
    except:
        pass
    
    try:
        student_name = request.session['student_name']  
    except:
        pass
    
    response = Student.objects.filter(student_num__startswith=student_name)
    result = []
    for re in response:
        if int(re.score) == 2:
            result.append("注意，你有可能挂科咯")
    request.session['result'] = result
    
    context = {
        "UserName":student_name,
        "result":result,
        }
    template = loader.get_template('student_client/index.html')
    return HttpResponse(template.render(context, request))

def Single_student(request):
    """
    @author: 
    @modify: jack
    @return: 填一下
    """
    
    template = loader.get_template('student_client/input.html')
    context = {
        'student_num':request.session['student_name'] ,
    }
    return HttpResponse(template.render(context, request))

def search_score(request):
    """
    @author: 
    @return: 填一下
    """
    from background_program.z_Tools.MyDataBase import MyDataBase
    
    try:
        student_name = request.session['student_name']  
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
