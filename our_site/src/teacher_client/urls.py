from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^show_infos$', views.show_infos, name='show_infos'),
]
