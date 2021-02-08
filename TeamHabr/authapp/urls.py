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
        authapp.Login.as_view(),
        name='login'),
    path(
        'logout/',
        authapp.Logout.as_view(),
        name='logout'),
    path(
        'register/',
        authapp.Register.as_view(),
        name='register'),
    path(
        'account/',
        login_required(
            authapp.Account.as_view()),
        name='account'),
]
