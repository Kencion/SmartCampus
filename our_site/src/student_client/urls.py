from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_score$', views.search_score, name='search_score'),
    url(r'^Single_student$', views.Single_student, name='Single_student'),
]
