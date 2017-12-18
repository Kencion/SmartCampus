from django.shortcuts import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect  
from student_client.models import Student
# Create your views here.

def index(request):
    """
    @author: Jack 
    @return: 主页
    """
    template = loader.get_template('index_page/index.html')
    return HttpResponse(template.render(None, request))

def login(request):
    """
    @author: Jack
    @return: 登录页面
    """
    template = loader.get_template('index_page/login.html')
    return HttpResponse(template.render(None, request))

def logout_view(request):
    """
    @author: 
    @return: 填一下
    """
    template = loader.get_template('index_page/login.html')
    try:
        del request.session['UserName']
    except KeyError:
        pass
    return HttpResponse(template.render(None, request))

def Login_judge(request):
    """
    @author: yhj
    @modify: jack
    @return: 填一下
    """
#     if request.session.get('UserName') is not None:
#         
    template = loader.get_template('index_page/Login.html')
    """用户名为空"""
    try:
        UserName = request.POST['UserName']
        if UserName == '':
            raise Exception
    except:
        context = {
            'result': "用户名不能为空",
            }
        return HttpResponse(template.render(context, request))
    
    """密码为空"""
    try:
        password = request.POST['password']
        if password == '':
            raise Exception
    except:
        context = {
        'result': "密码不能为空",
        }
        return HttpResponse(template.render(context, request))
    
    """身份为空"""
    try:
        Title_category = request.POST['Title_category'] 
    except:
        context = {
        'result': "请选择您的身份",
        }
        return HttpResponse(template.render(context, request)) 
    
    """正常情况"""    
    if Title_category == "student":       
        return HttpResponseRedirect('/student_client?user_name=' + UserName)
    else:
        return HttpResponseRedirect('/teacher_client?user_name=' + UserName)
