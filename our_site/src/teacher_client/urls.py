from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^class_failing_warning$', views.class_failing_warning, name='class_failing_warning'),
    url(r'^missing_warning$', views.missing_warning, name='missing_warning'),
    url(r'^scholarship_forcasting$', views.scholarship_forcasting, name='scholarship_forcasting'),
    url(r'^score_forcasting$', views.score_forcasting, name='score_forcasting'),
    
]
