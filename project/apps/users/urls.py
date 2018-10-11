from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('update', views.UserUpdateView.as_view(), name='update'),
    path('password', views.change_password, name='change-password'),
]
