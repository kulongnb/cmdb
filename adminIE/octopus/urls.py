from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from .views import ConnectionView,EexcCommand,asyncDemoView,get_task,ansible_api
app_name="octopus"
urlpatterns = [
    path("connection/",ConnectionView.as_view(),name='connection'),
    path("run/",EexcCommand.as_view(),name='run'),
    path("get_task/",get_task.as_view(),name='get_task'),
    path("async/",asyncDemoView.as_view(),name='asyncdemo'),
    path("ansible_api/",ansible_api.as_view(),name="ansible_api"),


]