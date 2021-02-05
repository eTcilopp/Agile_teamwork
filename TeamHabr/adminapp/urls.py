import adminapp.views as adminapp
from django.urls import path
app_name = 'adminapp'

"""
Ссылки на элементы приложения adminapp
"""

urlpatterns = [
    path(
        'category_list/',
        adminapp.AdminCategoryList.as_view(),
        name='category_list'),
    path(
        'user_list/',
        adminapp.AdminUserList.as_view(),
        name='user_list'),
    path(
        'post_list/',
        adminapp.AdminPostList.as_view(),
        name='post_list'),
    path(
        'create_category/',
        adminapp.AdminCreateCategory.as_view(),
        name='create_category'),

    path(
        'create_moder/<int:pk>/',
        adminapp.create_moder,
        name='create_moder'),

    path(
        'delete_moder/<int:pk>/',
        adminapp.delete_moder,
        name='delete_moder'),
]