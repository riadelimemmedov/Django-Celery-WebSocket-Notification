from django.urls import path
from .views import *

app_name='mainapp'
urlpatterns = [
    path('',homeView,name='homeView'),
    path('test/',testView,name='testView')
]
