from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show_student_info$', views.show_student_info, name='show_student_info'),
]
