from django.shortcuts import render
from django.views.generic import CreateView, ListView
from authapp.models import User
from mainapp.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin


class AdminUserList(LoginRequiredMixin, ListView):
    """
        Класс контроллера обрабоки запросов на просмотр главной станицы.
        Класс наследует от встроенного класса ListView
        Задается связанная модель
        Задается количество статей, выводимых на одном экране одновременно (пагинация)
        """
    template_name = "adminapp/user_list.html"
    model = User
    paginate_by = 4


class AdminPostList(LoginRequiredMixin, ListView):
    """
        Класс контроллера обрабоки запросов на просмотр главной станицы.
        Класс наследует от встроенного класса ListView
        Задается связанная модель
        Задается количество статей, выводимых на одном экране одновременно (пагинация)
        """
    template_name = "adminapp/post_list.html"
    model = Post
    paginate_by = 4


