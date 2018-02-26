from django.conf.urls import url
from . import views

app_name = "AskPete"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(r'^getquery/$', views.get_query, name='getquery'),
]
