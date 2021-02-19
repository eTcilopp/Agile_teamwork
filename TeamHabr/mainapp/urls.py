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
        'search_results',
        mainapp.Index.as_view(),
        name='search_results'),

    path(
        'category/<slug:slug>/',
        mainapp.Index.as_view(),
        name='category'),
    path(
        'search_results/<slug:slug>/',
        mainapp.Index.as_view(),
        name='search_results'),

    path(
        'main/<str:data_type>/',
        mainapp.Index.as_view(),
        name='popular'),
    path(
        'category/<slug:slug>/<str:data_type>/',
        mainapp.Index.as_view(),
        name='category_popular'),
    path(
        'post/create/',
        mainapp.ArticleCreate.as_view(),
        name='article_create'),

    path(
        'post/<slug:slug>/',
        mainapp.PostRead.as_view(),
        name='post'),

    path(
        'post/edit/<slug:slug>/',
        mainapp.ArticleUpdate.as_view(),
        name='article_edit'),

    path(
        'post/delete/<slug:slug>/',
        mainapp.ArticleDelete.as_view(),
        name='article_delete'),

    path(
        'like/<int:pk>/<str:type_likes>',
        mainapp.likes,
        name='like'),

    path(
        'help',
        mainapp.HelpPage.as_view(),
        name='help'),

]
