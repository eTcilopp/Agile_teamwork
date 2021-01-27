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
    path('design', mainapp.Design.as_view(), name='design'),
    path('mobile_development', mainapp.MobileDevelopment.as_view(), name='mobile_development'),
    path('web_development', mainapp.WebDevelopment.as_view(), name='web_development'),
    path('marketing', mainapp.Marketing.as_view(), name='marketing'),
    path('help_page', mainapp.HelpPage.as_view(), name='help_page'),
    path('article-create/', login_required(mainapp.ArticleCreate.as_view()), name='article-create'),

]
