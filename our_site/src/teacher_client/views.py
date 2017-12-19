from django.shortcuts import loader
from django.http import HttpResponse
import matplotlib.pyplot as plt
import numpy as np
import sys
from student_client.models import Student
from django.http.response import HttpResponseRedirect
# Create your views here.
 
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
        pass 
    
    """从数据库获得失联学生的学号"""
    context['student_nums'] = [i.student_num for i in Student.objects.filter(is_missing__exact=True)]

    """将数据渲染到页面上"""
    template = loader.get_template('teacher_client/index.html')
    return HttpResponse(template.render(context, request))
    

def score_forcasting(request, update=False):
    """
            成绩预测页面
    @author: Jack
    @return: 成绩预测页面
    """
    """
            获得所有学生的成绩预测结果，
            并在数据mydatabase表student_client_Student中
            将该学生的score字段设为预测结果
    """
    try:
        """如果需要更新数据"""
        update = request.GET['update']
        if update:
            pie_chart(), line_chart(), broken_line_chart()
            from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting
            students_and_scores = score_forcasting().doit()
            print(students_and_scores)
            for i in students_and_scores:
                Student(student_num=i[0], score=i[1]).save()
        return HttpResponseRedirect('/teacher_client/score_forcasting')
    except:
        pass
    
    students_and_scores = [[i.student_num, i.score] for i in Student.objects.all()]
    """获取挂科的同学的学号"""    
    class_fail_student_nums = [i.student_num for i in Student.objects.filter(score__lt=60.0)]

    """将数据渲染到页面上"""
    context = {
        'module_name':'成绩预测',
        'teacher_name':request.session['teacher_name'],
        'students_and_scores':students_and_scores,
        'class_fail_student_nums':class_fail_student_nums,
        }
    template = loader.get_template('teacher_client/score_forcasting.html')
    
    return HttpResponse(template.render(context, request))

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
    template = loader.get_template('teacher_client/missing_warning.html')
    
    return HttpResponse(template.render(context, request))
 
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
            students_and_scholarships = scholarship_forcasting().doit()
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
            students_and_subsidies = subsidy_forcasting().doit()
            for i in students_and_subsidies:
                Student(student_num=i[0], subsidy=i[1]).save()
        return HttpResponseRedirect('/teacher_client/subsidy_forcasting')
    except:
        pass
    
    students_and_subsidies = [[i.student_num, i.subsidy] for i in Student.objects.all()]

    """将数据渲染到页面上"""
    context = {
        'module_name':'助学金预测',
        'teacher_name':request.session['teacher_name'],
        'students_and_subsidies':students_and_subsidies,
        }
    template = loader.get_template('teacher_client/subsidy_forcasting.html')
    
    return HttpResponse(template.render(context, request))

"""下面是画图的函数"""
def broken_line_chart():
    """
    @author:yzh
    @modify: jack把这个函数的名字由zhexian_fig改成了 broken_line_chart
    @return: 填一下
    """
    from background_program.y_Modules.class_failing_warning.class_failing_warning import class_failing_warning
    
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
    @modify: jack把这个函数的名字由bingzhuang_fig改成了 pie_chart
    @return: 填一下
    """
    from background_program.y_Modules.class_failing_warning.class_failing_warning import class_failing_warning
    
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
    from background_program.y_Modules.score_forcasting.score_forcasting import score_forcasting
    
    t = score_forcasting()
    infos = t.doit()
    
    score = [x[1] for x in infos]
    x = range(101)
    y = np.zeros(101)
    for i in x:
        for j in score:
            if j >= (i - 0.5) and j < (i + 0.5):
                y[i] += 1
    fig = plt.figure('By SmartCampus Team')
    ax = fig.add_subplot(111)
    ticks = ax.set_xticks(np.linspace(0, 100, 21))
    plt.xlim(0, 100)
    ax.set_title('学生成绩分布折线图')
    ax.set_xlabel('成绩')
    ax.set_ylabel('学生数量')
    plt.ylim(0, max(y) * 1.1)
    ax.plot(x,y,linewidth =2 ,color = '#436EEE') 
    
    ax.fill(x, y, color='#00B2EE')
    save_path = sys.path[0] + '/teacher_client/static/teacher_client/images/line_chart.png'
    plt.legend()
    plt.savefig(save_path)
    # plt.show()
    plt.close()
