from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('q=<question>/', views.question_detail, name='detail'),

]