from django.shortcuts import loader
from django.http import HttpResponse

# Create your views here.
def index(request):
    template = loader.get_template('teacher_client/index.html')
    context = {
        'title': "hello, my dear teacher, please click the button: ",
    }
    return HttpResponse(template.render(context, request))

def show_infos(request):
    from background_program.y_Modules.ClassFailingWarning.ClassFailingWarning import ClassFailingWarning
    
    t = ClassFailingWarning()
    print(type(t))
    infos = t.doit()
    template = loader.get_template('teacher_client/show_infos.html')
    context = {
        'infos': infos,
    }
    return HttpResponse(template.render(context, request))
