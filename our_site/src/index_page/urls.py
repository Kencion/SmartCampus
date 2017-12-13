from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^Login_judge$', views.Login_judge, name='Login_judge'),
    url(r'^logout_view$', views.logout_view, name='logout_view'),
]
