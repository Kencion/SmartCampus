from django.shortcuts import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect  

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
    template = loader.get_template('index_page/login.html')
    try:
        del request.session['UserName']
    except KeyError:
        pass
    return HttpResponse(template.render(None, request))
def Login_judge(request):
    """
    @author: 
    @return: 填一下
    """
    if request.session.get('UserName') is not None:
        if request.session['Title_category']=='student':
            template = loader.get_template('student_client/index.html')
            context = {
            "UserName":request.session.get('UserName'),
            "password":request.session.get('password'),
            }
            return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('teacher_client/index.html')
            context = {
            "UserName":request.session.get('UserName'),
            "password":request.session.get('password'),
            }
            return HttpResponse(template.render(context, request))
    else:
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
            template = loader.get_template('student_client/index.html')
            request.session['UserName'] = UserName
            request.session['password'] = password
            request.session['Title_category'] = Title_category
            context = {
                "UserName":UserName,
                "password":password,
                }
            return HttpResponse(template.render(context, request))
        else:
#             template = loader.get_template('teacher_client/index.html')
            request.session['UserName'] = UserName
            request.session['password'] = password
            request.session['Title_category'] = Title_category
            context = {
                "UserName":UserName,
                "password":password,
                }
            return HttpResponseRedirect('/teacher_client/')
#             return HttpResponse(template.render(context, request))
