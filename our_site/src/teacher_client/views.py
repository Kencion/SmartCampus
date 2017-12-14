from django.shortcuts import loader
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import sys
from background_program.y_Modules.class_failing_warning.class_failing_warning import class_failing_warning
from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting
# Create your views here.
 
def index(request):
    """
            教师端的主页
    @author: Jack
    @return 教师端的主页
    """
    from student_client.models import Student

    """从数据库获得失联学生的学号"""
    student_nums = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]

    print(student_nums)

    """将数据渲染到页面上"""
    context = {
        'teacher_name':'我是一个老师',
        'student_nums':student_nums,
        }
    
    template = loader.get_template('teacher_client/index.html')
    return HttpResponse(template.render(context, request))
 
def class_failing_warning(request):
    """
            挂科预警页面
    @author: Jack
    @return: 挂科预警页面
    """
    from background_program.y_Modules.class_failing_warning.class_failing_warning import class_failing_warning
    from student_client.models import Student
 
#     broken_line_chart()
#     pie_chart()
     
    """获取挂科预警的预测结果"""
    all_students = class_failing_warning().doit()
    types = set([i[1] for i in all_students])  # 按成绩来统计学生的不同类别
    students_and_scores = dict()  # 分别收集每种类别的学生
    for i in types:
        students_and_scores[i] = []
    for i in all_students:
        students_and_scores[i[1]].append(i[0])
        student = Student(student_num=i[0], score=i[1])
        student.save()
    
    """将数据渲染到页面上"""
    context = {
        'module_name':'挂科预警',
        'teacher_name':'我是一个老师',
        'students_and_scores':students_and_scores,
        'n_types':100.0 / len(types),
        }
     
    template = loader.get_template('teacher_client/class_failing_warning.html')
    return HttpResponse(template.render(context, request))
 
def missing_warning(request):
    """
            失联预警页面
    @author: Jack
    @return: 失联预警页面
    """
    from background_program.y_Modules.missing_warning import missing_warning
    from student_client.models import Student
    
    """
            获得可能失联的学生的学号，
            并在数据mydatabase表student_client_Student中
            将该学生的is_missing字段设为True
    """
    missing_students = missing_warning.doit()
    for i in missing_students:
        Student(student_num=i, is_missing=True).save()
    
    """将数据渲染到页面上"""
    context = {
        'module_name':'失联预警',
        'teacher_name':'我是一个老师',
        'student_nums':missing_students,
        }
    
    template = loader.get_template('teacher_client/missing_warning.html')
    return HttpResponse(template.render(context, request))
 
def score_forcasting(request):
    """
            成绩预测页面
    @author: Jack
    @return: 成绩预测页面
    """
    from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting
    from student_client.models import Student
    
    
    """
            获得可能失联的学生的学号，
            并在数据mydatabase表student_client_Student中
            将该学生的is_missing字段设为True
    """
    students_and_scores = score_forcasting('score').doit()
#     for i in students_and_scores:
#         Student(student_num=i[0], score=i[1]).save
    
    """将数据渲染到页面上"""
    context = {
        'module_name':'成绩预测',
        'teacher_name':'我是一个老师',
        'students_and_scores':students_and_scores,
        }
    
    template = loader.get_template('teacher_client/score_forcasting.html')
    return HttpResponse(template.render(context, request))

def scholarship_forcasting(request):
    """
            挂科预警页面
    @author: Jack
    @return: 挂科预警页面
    """
    from background_program.y_Modules.scholarship_forcasting.scholarship_forcasting import scholarship_forcasting
 
#     broken_line_chart()
#     pie_chart()
     
    """获取挂科预警的预测结果"""
    all_students = class_failing_warning().doit()
    types = set([i[1] for i in all_students])  # 按成绩来统计学生的不同类别
    infos = dict()  # 分尅收集每种类别的学生
    for i in types:
        infos[i] = []
    for i in all_students:
        infos[i[1]].append(i[0])
        
    """将数据渲染到页面上"""
    context = {
        'module_name':'挂科预警',
        'teacher_name':'我是一个老师',
        'infos':infos,
        }
     
    template = loader.get_template('teacher_client/scholarship_forcasting.html')
    return HttpResponse(template.render(context, request))
 
 
def broken_line_chart():
    """
<<<<<<< HEAD
    @author:
=======
            名字可以
    @author:yzh
>>>>>>> a92968790935648883560ce555f16c93620cde7f
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
    @author: yzh
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
def line_chart():
    """
    @author: yzh
    @return: 填一下
    """
    t = score_forcasting('score')
    infos = t.doit()
    
    score = [x[1] for x in infos]
    x = range(101)
    y = np.zeros(101)
    for i in x:
        for j in score:
            if j>=(i-0.5) and j<(i+0.5):
                y[i]+=1
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ticks = ax.set_xticks(np.linspace(0,100,21))
    plt.xlim(0,100)
    ax.set_title('学生成绩分布折线图')
    ax.set_xlabel('成绩')
    ax.set_ylabel('学生数量')
    plt.ylim(0,max(y)*1.1)
    ax.plot(x,y,color = 'skyblue') 
    
    ax.fill(x,y,color = 'skyblue')
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/line_chart.png'
    plt.legend()
    plt.savefig(save_path)
    # plt.show()
    plt.close()