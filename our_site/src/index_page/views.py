from django.shortcuts import loader
from django.http import HttpResponse

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