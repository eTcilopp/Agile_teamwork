from django.contrib import admin
from django.urls import path

import authapp.views as authapp

app_name = 'authapp'

"""
ТЕКСТ
"""
urlpatterns = [
    path('login/', authapp.Login.as_view(), name='login'),
    path('logout/', authapp.Logout.as_view(), name='logout'),
    path('register/', authapp.Register.as_view(), name='register'),
]
