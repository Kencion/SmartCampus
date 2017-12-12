from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^class_failing_warning$', views.class_failing_warning, name='class_failing_warning'),
]
