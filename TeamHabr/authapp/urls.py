from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
import authapp.views as authapp

app_name = 'authapp'

"""
Ссылки на элементы приложения authapp
login - Создание процедуры Авторизации 
logout - Процедура разлогинивания
register - Создание процедуры Регистрации
account - Вывод страницы личного кабинета
"""

urlpatterns = [
    path(
        'login/',
        authapp.LoginView.as_view(), name='login'),
    path(
        'logout/',
        authapp.Logout.as_view(),
        name='logout'),
    path(
        'register/',
        authapp.Register.as_view(),
        name='register'),
    path('activate/<uidb64>/<token>/',
         authapp.Activate.as_view(),
         name='activate'),
    path(
        'account/',
        login_required(
            authapp.Account.as_view()),
        name='account'),
    path(
        'edit/',
        authapp.Edit.as_view(),
        name='edit',),
    path('update/',
         authapp.UserUpdate.as_view(),
         name='edit')
]
