from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

"""
Ссылки на элементы приложения mainapp
index - Генерация главной страницы 
category - Генерация тематических разделов
article_create - Создание новой статьи
post - Вывод индививдуальной статьи
help - Страница помощи
"""

urlpatterns = [

    path(
        '',
        mainapp.Index.as_view(),
        name='index'),

    path(
        'category/<slug:slug>/',
        mainapp.Index.as_view(),
        name='category'),


    path(
        'post/create/',
        login_required(mainapp.ArticleCreate.as_view()),
        name='article_create'),

    path(
        'post/<slug:slug>/',
        mainapp.PostRead.as_view(),
        name='post'),

    path(
        'help',
        mainapp.HelpPage.as_view(),
        name='help'),

]
