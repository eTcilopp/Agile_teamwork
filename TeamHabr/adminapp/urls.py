import adminapp.views as adminapp
from django.urls import path
app_name = 'adminapp'

"""
Ссылки на элементы приложения adminapp
"""

urlpatterns = [
    path(
        'user_list/',
        adminapp.AdminUserList.as_view(),
        name='user_list'),
    path(
        'post_list/',
        adminapp.AdminPostList.as_view(),
        name='post_list'),
]