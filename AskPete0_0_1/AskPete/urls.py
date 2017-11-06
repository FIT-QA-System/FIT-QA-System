from django.conf.urls import url
from . import views

app_name = "AskPete"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<input_text>)getquery/$', views.get_query, name='getquery'),
]
