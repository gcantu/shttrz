from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('home', views.Home, name='home'),
    path('settings', views.Settings, name='settings'),
    path('success', views.Success, name='success'),
]
