from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^class_failing_warning$', views.class_failing_warning, name='class_failing_warning'),
    url(r'^r$', views.r, name='r'),  # 什么意思
    url(r'^show_infos$', views.show_infos, name='show_infos'),
    url(r'^Single_student$', views.Single_student, name='Single_student'),
    url(r'^show_student$', views.show_student, name='show_student'),
    url(r'^bingzhuang_fig$', views.bingzhuang_fig, name='bingzhuang_fig'),
    url(r'^zhexian_fig$', views.zhexian_fig, name='zhexian_fig'),
]
