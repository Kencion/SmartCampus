from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^score_forcasting$', views.score_forcasting, name='score_forcasting'),
    url(r'^missing_warning$', views.missing_warning, name='missing_warning'),
    url(r'^scholarship_forcasting$', views.scholarship_forcasting, name='scholarship_forcasting'),
    url(r'^subsidy_forcasting$', views.subsidy_forcasting, name='subsidy_forcasting'),
    url(r'^wired_person$', views.wired_person, name='wired_person'),
    url(r'^student_info$', views.student_info, name='student_info'),
    url(r'^not_login$', views.not_login, name='not_login'),
]
