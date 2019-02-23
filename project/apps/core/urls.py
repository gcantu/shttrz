from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('home', views.Home, name='home'),
    path('success', views.Success, name='success'),
]
