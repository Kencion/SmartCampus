from django.shortcuts import loader
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import os, sys
from background_program.y_Modules.class_failing_warning.class_failing_warning import class_failing_warning
# Create your views here.
 
def index(request):
    """
    @author: Jack
    @return 教师端的主页
    """
    template = loader.get_template('teacher_client/index.html')
    return HttpResponse(template.render(None, request))
 
def class_failing_warning(request):
    """
    @author: Jack
    @return: 挂科预警页面
    """
    from background_program.y_Modules.class_failing_warning.class_failing_warning import class_failing_warning
 
#     broken_line_chart()
#     pie_chart()
     
    template = loader.get_template('teacher_client/class_failing_warning.html')
     
    """获取挂科预警的预测结果"""
    all_students = class_failing_warning().doit()
    types = set([i[1] for i in all_students])  # 按成绩来统计学生的不同类别
    infos = dict()  # 分尅收集每种类别的学生
    for i in types:
        infos[i] = []
    for i in all_students:
        infos[i[1]].append(i[0])
    
    context = {
        'module_name':'挂科预警',
        'teacher_name':'我是一个老师',
        'infos':infos,
        'n_types':100.0 / len(types),
        }
     
    return HttpResponse(template.render(context, request))
 
def missing_warning(request):
    """
    @author: Jack
    @return: 失联预警页面
    """
    from background_program.y_Modules.missing_warning import missing_warning
    
    template = loader.get_template('teacher_client/missing_warning.html')
    
    student_nums = missing_warning.doit()
    
    context = {
        'module_name':'失联预警',
        'teacher_name':'我是一个老师',
        'student_nums':student_nums,
        }
    return HttpResponse(template.render(context, request))
 

def scholarship_forcasting(request):
    """
    @author: Jack
    @return: 挂科预警页面
    """
    from background_program.y_Modules.scholarship_forcasting.scholarship_forcasting import scholarship_forcasting
 
#     broken_line_chart()
#     pie_chart()
     
    template = loader.get_template('teacher_client/scholarship_forcasting.html')
     
    """获取挂科预警的预测结果"""
    all_students = class_failing_warning().doit()
    types = set([i[1] for i in all_students])  # 按成绩来统计学生的不同类别
    infos = dict()  # 分尅收集每种类别的学生
    for i in types:
        infos[i] = []
    for i in all_students:
        infos[i[1]].append(i[0])
    
    for i in infos:
        print(i + 1)
#         for j in infos.get(i):
#             print(j)
    
    context = {
        'module_name':'挂科预警',
        'teacher_name':'我是一个老师',
        'infos':infos,
        }
     
    return HttpResponse(template.render(context, request))
 
 
def broken_line_chart():
    """
            名字可以
    @author:
    @change: jack把这个函数的名字由zhexian_fig改成了 broken_line_chart
    @return: 填一下
    """
    t = class_failing_warning()
    infos = t.doit()
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 4., 1.01 * height, "%s" % float(height))
    num = np.zeros(5)
    score = [x[1] for x in infos]
     
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Bar Chart')
    colors = ['red', 'yellowgreen', 'lightskyblue', 'g', 'b']
    labels = [u"0类", u"1类", u"2类", u"3类", u"4类"]
    rec = plt.bar(labels, num, color=colors) 
    autolabel(rec)
    ax.set_xlabel('Student type')
    ax.set_ylabel('Student number')
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/broken_line_chart.png'
    plt.savefig(save_path)
    plt.close()
 
def pie_chart():
    """
    @author: 
    @change: jack把这个函数的名字由bingzhuang_fig改成了 pie_chart
    @return: 填一下
    """
    t = class_failing_warning()
    infos = t.doit()
    num = np.zeros(5)
    colors = ['red', 'yellowgreen', 'lightskyblue', 'g', 'b']
    labels = [u"0类", u"1类", u"2类", u"3类", u"4类"]
    score = [x[1] for x in infos]
    for i in range(5):
        num[i] = score.count(i)
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ax.set_title('Pie Chart')
    patches, l_text, p_text = plt.pie(num, labels=labels, colors=colors, labeldistance=1.1, autopct='%3.1f%%', shadow=False, startangle=90, pctdistance=0.6) 
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/pie_chart.png'
    for t in l_text:
        t.set_size = (30)
    for t in p_text:
        t.set_size = (20)
# 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend()
    plt.savefig(save_path)
#     plt.show()
    plt.close()
