#coding:UTF-8
from django.shortcuts import loader
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import os, sys
from django.shortcuts import render
from PIL import Image
import threading
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
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x()+rect.get_width()/4., 1.01*height, "%s" % float(height))
    num = np.zeros(5)
    score = [x[1] for x in infos]
    
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Bar Chart')
    colors = ['red','yellowgreen','lightskyblue','g','b']
    labels = [u"0类",u"1类",u"2类",u"3类",u"4类"]
    rec = plt.bar(labels, num, color=colors) 
    autolabel(rec)
    ax.set_xlabel('Student type')
    ax.set_ylabel('Student number')
    save_path = sys.path[0]+'/teacher_client/static/teacher_client/images/zhexian.png'
    plt.savefig(save_path)
    plt.close()
    context = {
        'infos': infos,
    }
    return HttpResponse(template.render(context, request))
def bingzhuang_fig(request):
    template=loader.get_template('teacher_client/bingzhuang_fig.html')
    from background_program.y_Modules.ClassFailingWarning.ClassFailingWarning import ClassFailingWarning
    t = ClassFailingWarning()
    infos = t.doit()
    num = np.zeros(5)
    colors = ['red','yellowgreen','lightskyblue','g','b']
    labels = [u"0类",u"1类",u"2类",u"3类",u"4类"]
    score = [x[1] for x in infos]
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Pie Chart')
    patches,l_text,p_text = plt.pie(num,labels = labels,colors=colors,labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,startangle = 90,pctdistance = 0.6) 
    save_path = sys.path[0]+'/teacher_client/static/teacher_client/images/bingzhuang.png'
    for t in l_text:
        t.set_size=(30)
    for t in p_text:
        t.set_size=(20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend()
    plt.savefig(save_path)
#     plt.show()
    plt.close()
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