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
#传入username，返回学号对应的学生信息的键值对
def Search_student_info(request):
    from background_program.z_Tools.my_database import MyDataBase
    try:
        student_num = request.GET['user_name']
        db = MyDataBase("软件学院")
        executer = db.getExcuter()
        sql="select * from students where student_num={0}".format(student_num)
        executer.execute(sql)
        student = list(executer.fetchone())
        column_name=['学号','姓名','学生类别','学年参与活动数量','参与活动的平均活跃程度','活动持续时间','活动平均参与分','表彰级别',\
                     '平均每学年获荣誉次数','图书借阅次数','学年学习总时间','周末自习时间','GPA','成绩排名','助学金等级','助学金金额','挂科科目数',\
                     '重修通过的科目数量','重修未过的科目数量','社会实践参与总时间','社会实践参与是否重点','平均每日进出次数','学年','奖学金等级','奖学金金额',\
                     '成绩','周末平均最早出宿舍时间','平均周末最迟回宿舍时间','工作日平均在外时间','食堂总消费额','超市总消费额','其他类别总消费额','充值总额','小吃消费总额',\
                     '锻炼总消费额','学习消费总额','充值日平均消费额最大值','锻炼日消费最大值','小吃日消费最大值','学习日消费最大值','超市日消费最大值','餐厅日消费最大值','其他类别日消费最大值',\
                     '充值月消费最大值','锻炼月消费最大值','小吃月消费最大值','学习月消费最大值','食堂月消费最大值','超市月消费最大值','其他类别月消费最大值','充值月消费最小值','锻炼月消费最小值','小吃月消费最小值',\
                     '学习月消费最小值','食堂月消费最小值','超市月消费最小值','其他类别月消费最小值','总消费次数','食堂消费额占总消费额的比例','食堂消费次数','总消费额','食堂消费的中位数','超市消费的中位数','充值消费的中位数','小吃消费的中位数',\
                     '锻炼消费的中位数','学习消费的中位数','其他类别消费的中位数','食堂消费的平均值','超市消费的平均值','充值消费的平均值','小吃消费的平均值',\
                     '锻炼消费的平均值','学习消费的平均值','其他类别消费的平均值','食堂消费的方差','超市消费的方差','充值消费的方差','其他类别消费的方差','小吃消费的方差',\
                     '锻炼消费的方差','学习消费的方差']
        result={}
        for i in range(len(student)):
            result[column_name[i]]=student[i]
        return result
    except:
        pass
    
def show_student_info(request):
    from background_program.z_Tools.my_database import MyDataBase
    student_num=request.session.get('student_num')
    db = MyDataBase("软件学院")
    executer = db.getExcuter()
#     sql = "select * from students where student_num like '{0}%'".format(student_num)
#     executer.execute(sql)
#     students_list = executer.fetchall()
#     student_name=students_list[0][1]
#     print(students_list)
#     db.close 
    sql="select * from students where student_num like '{0}%'".format(student_num)
    executer.execute(sql)
    student = executer.fetchone()
    column_name=['学号','姓名','学生类别','学年参与活动数量','参与活动的平均活跃程度','活动持续时间','活动平均参与分','表彰级别',\
                 '平均每学年获荣誉次数','图书借阅次数','学年学习总时间','周末自习时间','GPA','成绩排名','助学金等级','助学金金额','挂科科目数',\
                 '重修通过的科目数量','重修未过的科目数量','社会实践参与总时间','社会实践参与是否重点','平均每日进出次数','学年','奖学金等级','奖学金金额',\
                 '成绩','周末平均最早出宿舍时间','平均周末最迟回宿舍时间','工作日平均在外时间','食堂总消费额','超市总消费额','其他类别总消费额','充值总额','小吃消费总额',\
                 '锻炼总消费额','学习消费总额','充值日平均消费额最大值','锻炼日消费最大值','小吃日消费最大值','学习日消费最大值','超市日消费最大值','餐厅日消费最大值','其他类别日消费最大值',\
                 '充值月消费最大值','锻炼月消费最大值','小吃月消费最大值','学习月消费最大值','食堂月消费最大值','超市月消费最大值','其他类别月消费最大值','充值月消费最小值','锻炼月消费最小值','小吃月消费最小值',\
                 '学习月消费最小值','食堂月消费最小值','超市月消费最小值','其他类别月消费最小值','总消费次数','食堂消费额占总消费额的比例','食堂消费次数','总消费额','食堂消费的中位数','超市消费的中位数','充值消费的中位数','小吃消费的中位数',\
                 '锻炼消费的中位数','学习消费的中位数','其他类别消费的中位数','食堂消费的平均值','超市消费的平均值','充值消费的平均值','小吃消费的平均值',\
                 '锻炼消费的平均值','学习消费的平均值','其他类别消费的平均值','食堂消费的方差','超市消费的方差','充值消费的方差','其他类别消费的方差','小吃消费的方差',\
                 '锻炼消费的方差','学习消费的方差',]
    result={}
    for i in range(len(student)):
        if student[i] is None:
            result[column_name[i]]='None'
        else:
            result[column_name[i]]=student[i]
    template = loader.get_template('student_client/show_student_info.html')
    context = {
        'UserName':student_num,
        'result':result,
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
        'UserName':request.session['student_num'],
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
            'UserName':student[0],
            'student_num':student[0],
            'student_name':student[1],
            'student_grade':student[2],
            'score_rank':student[3],
            'score':student[4],
        }
        return HttpResponse(template.render(context, request))
