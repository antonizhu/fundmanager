from django.contrib import admin
from django.urls import path
from services import views

app_name = 'services'
urlpatterns = [
    path('', views.index, name='index'),
    path('makeTransaction', views.makeTransaction, name='makeTransaction'),
    path('report', views.report, name='report'),
]