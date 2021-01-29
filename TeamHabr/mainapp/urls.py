from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

"""
ТЕКСТ
"""
urlpatterns = [

    path('', mainapp.Index.as_view(), name='index'),
    path('category/<str:slug>/', mainapp.Index.as_view(), name='by_category'),
    path('help_page', mainapp.HelpPage.as_view(), name='help_page'),
    path('article-create/', login_required(mainapp.ArticleCreate.as_view()), name='article-create'),
    path('post/<slug:slug>/', mainapp.PostRead.as_view(), name='post'),

]
