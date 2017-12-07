from django.shortcuts import render, loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    template = loader.get_template('student_client/index.html')
    context = {
        'title': "hello, my dear student, please input your student_num and school_year: ",
    }
    return HttpResponse(template.render(context, request))

def show_student_info(request):
    from background_program.z_Tools.MyDataBase import MyDataBase
    
    student_num = request.POST['student_num']
    year=request.POST['year']
    student_num=student_num+year
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
    sql = "select student_num,student_name,score_rank,score from students where student_num='{0}'".format(student_num)
    executer.execute(sql)
    student = executer.fetchone()
    db.close 
    print(student)
    if student is None:
        template = loader.get_template('student_client/index.html')
        context={
            'title':"hello, my dear student, please input your student_num and school_year: ",
            'result':"Sorry,I can't find the student_num or shool_year.",
            }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('student_client/show_student_info.html')
        context = {
            'student_num':student[0],
            'student_name':student[1],
            'score_rank':student[2],
            'score':student[3],
        }
        return HttpResponse(template.render(context, request))
    
