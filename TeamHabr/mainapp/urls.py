from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'

"""
ТЕКСТ
"""
urlpatterns = [
    path('', mainapp.index, name='index'),
    path('design', mainapp.design, name='design'),
    path('mobile_development', mainapp.mobile_development, name='mobile_development'),
    path('web_development', mainapp.web_development, name='web_development'),
    path('marketing', mainapp.marketing, name='marketing'),
    path('help_page', mainapp.help_page, name='help_page'),
    path('account/', login_required(mainapp.Account.as_view()), name='account'),
    path('article-create/', login_required(mainapp.ArticleCreate.as_view()), name='article-create'),
]
