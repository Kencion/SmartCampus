from django.shortcuts import loader
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import os, sys
from django.shortcuts import render
from PIL import Image
from multiprocessing.sharedctypes import template
# Create your views here.
def index(request):
    template = loader.get_template('teacher_client/index.html')
    context = {
        'title': "hello, my dear teacher, please click the button: ",
    }
    return HttpResponse(template.render(context, request))
def Login(request):
    template = loader.get_template('teacher_client/Login.html')
    context = {
        'title': "hello, my dear teacher, please click the button: ",
    }
    return HttpResponse(template.render(context, request))
def zhexian_fig(request):
    template=loader.get_template('teacher_client/zhexian_fig.html')
    from background_program.y_Modules.ClassFailingWarning.ClassFailingWarning import ClassFailingWarning
    t = ClassFailingWarning()
    infos = t.doit()
    num = np.zeros(5)
    score = [x[1] for x in infos]
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Bar Chart')
    plt.bar(range(len(num)), num, color='rgb') 
    ax.set_ylabel('Student number')
#     save_path = r'D:/zhexian.png'
#     plt.savefig(save_path)
#     img=Image.open(r'D:/zhexian.png')
#     img.save(sys.path[0]+r'/teacher_client/static/teacher_client/images/zhexian.png')
    context = {
        'infos': infos,
    }
    return HttpResponse(template.render(context, request))
def bingzhuang_fig(request):    
     from background_program.y_Modules.ClassFailingWarning.ClassFailingWarning import ClassFailingWarning
     template=loader.get_template('teacher_client/bingzhuang_fig.html')
     t = ClassFailingWarning()
     infos = t.doit()
     num = np.zeros(5)
     score = [x[1] for x in infos]
     for i in range(5):
         num[i] = score.count(i)
#      fig = plt.figure('By SmartCampus Team')
#      ax = fig.add_subplot(111)
#      ax.set_title('Pie Chart')
#      plt.pie(num,labels = range(len(num)),colors='rgb') 
#      save_path = r'D:/bingzhuang.png'
#      plt.savefig(save_path)
#      img=Image.open(r'D:/bingzhuang.png')
#      img.save(sys.path[0]+r'/teacher_client/static/teacher_client/images/bingzhuang.png')
     context = {
         'infos': infos,
     }
     return HttpResponse(template.render(context, request))
def Single_student(request):
    template = loader.get_template('teacher_client/input.html')
    context = {
        'title': "hello, my dear student, please input your student_num and school_year: ",
    }
    return HttpResponse(template.render(context, request))
def show_student(request):
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
    #print(student)
    if student is None:
        template = loader.get_template('teacher_client/input.html')
        context={
            'title':"hello, my dear student, please input your student_num and school_year: ",
            'result':"Sorry,I can't find the student_num or shool_year.",
            }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('teacher_client/show_student.html')
        context = {
            'student_num':student[0],
            'student_name':student[1],
            'score_rank':student[2],
            'score':student[3],
        }
        return HttpResponse(template.render(context, request))
def show_infos(request):
    from background_program.y_Modules.ClassFailingWarning.ClassFailingWarning import ClassFailingWarning
    
    t = ClassFailingWarning()
    #print(type(t))
    infos = t.doit()
    template = loader.get_template('teacher_client/show_infos.html')
    context = {
        'infos': infos,
    }
    return HttpResponse(template.render(context, request))
def r(request):
    UserName= request.POST['UserName']
    password= request.POST['password']
    Title_category= request.POST['Title_category'] 
    if request.POST['UserName']=='':
        template = loader.get_template('teacher_client/Login.html')
        context = {
        'result': "用户名不能为空",
        }
        return HttpResponse(template.render(context, request))
    elif password=='':
        template = loader.get_template('teacher_client/Login.html')
        context = {
        'result': "密码不能为空",
        }
        return HttpResponse(template.render(context, request))    
    if Title_category=="student":        
        template = loader.get_template('teacher_client/input.html')
        context = {
            "UserName":UserName,
            "password":password,
            }
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('teacher_client/index.html')
        context = {
            "UserName":UserName,
            "password":password,
            }
        return HttpResponse(template.render(context, request))